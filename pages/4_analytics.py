import streamlit as st
from lida import Manager, TextGenerationConfig, llm
from lida.datamodel import Goal
import os
import pandas as pd


# make data dir if it doesn't exist
os.makedirs("data", exist_ok=True)


st.header("LIDA: Automatic Generation of Visualizations and Infographics")


st.write("LIDA, an acronym for Language-based Interactive Data Analytics, is a tool developed by Microsoft Research and is designed for automatic data exploration and visualization using large language models (LLMs) like ChatGPT")


st.subheader("Why have we used Microsoft LIDA?")
st.write("Our aim was to create an advanced analytics tool for invoice processing.")
st.write("This is the last part of the tool where we visualize the data that we have extracted from the invoice.")



# Step 1 - Get OpenAI API key
openai_key = "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"


# Step 2 - Select a dataset and summarization method
if openai_key:
    # Initialize selected_dataset to None
    selected_dataset = None
    # set use_cache in sidebar
    use_cache = st.checkbox("Use cache", value=True)

    # Handle dataset selection and upload
    st.write("## Data Summarization")
    st.write("### Choose a dataset")

    datasets = [
        {"label": "Select a dataset", "url": None},
        {"label": "Cars", "url": "https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv"},
        {"label": "Weather", "url": "https://raw.githubusercontent.com/uwdata/draco/master/data/weather.json"},
    ]

    selected_dataset_label = st.selectbox(
        'Choose a dataset',
        options=[dataset["label"] for dataset in datasets],
        index=0
    )

    upload_own_data = st.checkbox("Upload your own data")

    if upload_own_data:
        uploaded_file = st.file_uploader("Choose a CSV or JSON file", type=["csv", "json"])

        if uploaded_file is not None:
            # Get the original file name and extension
            file_name, file_extension = os.path.splitext(uploaded_file.name)

            # Load the data depending on the file type
            if file_extension.lower() == ".csv":
                data = pd.read_csv(uploaded_file)
            elif file_extension.lower() == ".json":
                data = pd.read_json(uploaded_file)

            # Save the data using the original file name in the data dir
            uploaded_file_path = os.path.join("data", uploaded_file.name)
            data.to_csv(uploaded_file_path, index=False)

            selected_dataset = uploaded_file_path

            datasets.append({"label": file_name, "url": uploaded_file_path})

            # st.sidebar.write("Uploaded file path: ", uploaded_file_path)
    else:
        selected_dataset = datasets[[dataset["label"]
                                     for dataset in datasets].index(selected_dataset_label)]["url"]

    if not selected_dataset:
        st.info("To continue, select a dataset or upload your own.")


# Step 3 - Generate data summary
if openai_key and selected_dataset:
    lida = Manager(text_gen=llm("openai", api_key=openai_key))
    textgen_config = TextGenerationConfig(
        n=1,
        temperature=0.1,
        model="gpt-3.5-turbo",
        use_cache=use_cache)

    st.write("## Summary")
    # **** lida.summarize *****
    summary = lida.summarize(
        selected_dataset,
        summary_method="llm",
        textgen_config=textgen_config)

    if "dataset_description" in summary:
        st.write(summary["dataset_description"])

    if "fields" in summary:
        fields = summary["fields"]
        nfields = []
        for field in fields:
            flatted_fields = {}
            flatted_fields["column"] = field["column"]
            # flatted_fields["dtype"] = field["dtype"]
            for row in field["properties"].keys():
                if row != "samples":
                    flatted_fields[row] = field["properties"][row]
                else:
                    flatted_fields[row] = str(field["properties"][row])
            # flatted_fields = {**flatted_fields, **field["properties"]}
            nfields.append(flatted_fields)
        nfields_df = pd.DataFrame(nfields)
        st.write(nfields_df)
    else:
        st.write(str(summary))

    # Step 4 - Generate goals
    if summary:
        st.write("### Goal Selection")

        num_goals = st.slider(
            "Number of goals to generate",
            min_value=1,
            max_value=10,
            value=4)
        own_goal = st.checkbox("Add Your Own Goal")

        # **** lida.goals *****
        goals = lida.goals(summary, n=num_goals, textgen_config=textgen_config)
        st.write(f"## Goals ({len(goals)})")

        default_goal = goals[0].question
        goal_questions = [goal.question for goal in goals]

        if own_goal:
            user_goal = st.text_input("Describe Your Goal")

            if user_goal:
                new_goal = Goal(question=user_goal, visualization=user_goal, rationale="")
                goals.append(new_goal)
                goal_questions.append(new_goal.question)

        selected_goal = st.selectbox('Choose a generated goal', options=goal_questions, index=0)

        # st.markdown("### Selected Goal")
        selected_goal_index = goal_questions.index(selected_goal)
        st.write(goals[selected_goal_index])

        selected_goal_object = goals[selected_goal_index]

        # Step 5 - Generate visualizations
        if selected_goal_object:
            st.write("## Visualization Library")
            visualization_libraries = ["seaborn", "matplotlib", "plotly"]

            selected_library = st.selectbox(
                'Choose a visualization library',
                options=visualization_libraries,
                index=0
            )

            # Update the visualization generation call to use the selected library.
            st.write("## Visualizations")

            # slider for number of visualizations
            num_visualizations = st.slider(
                "Number of visualizations to generate",
                min_value=1,
                max_value=10,
                value=2)

            textgen_config = TextGenerationConfig(
                n=num_visualizations, temperature=0.1,
                model="gpt-3.5-turbo",
                use_cache=use_cache)

            # **** lida.visualize *****
            visualizations = lida.visualize(
                summary=summary,
                goal=selected_goal_object,
                textgen_config=textgen_config,
                library=selected_library)

            viz_titles = [f'Visualization {i+1}' for i in range(len(visualizations))]

            selected_viz_title = st.selectbox('Choose a visualization', options=viz_titles, index=0)

            selected_viz = visualizations[viz_titles.index(selected_viz_title)]

            if selected_viz.raster:
                from PIL import Image
                import io
                import base64

                imgdata = base64.b64decode(selected_viz.raster)
                img = Image.open(io.BytesIO(imgdata))
                st.image(img, caption=selected_viz_title, use_column_width=True)

            st.write("### Visualization Code")
            st.code(selected_viz.code)
