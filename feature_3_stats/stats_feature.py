import streamlit as st
import pandas as pd
import plotly.express as px

from core_db.db_config import get_db

def load_css():
    with open("feature_3_stats/analytics.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

def show_stats_page():

    load_css()

    col1, col2 = st.columns([2,1])

    with col1:

        st.markdown("""
        <div style="padding-top:50px;">

        <h1 style="
        font-size:100px;
        font-weight:900;
        color:white;
        line-height:1;
        text-shadow:
        0 0 20px #6AA8FF,
        0 0 60px #6AA8FF;
        ">
        GeneVault
        </h1>

        <h2 style="
        color:white;
        font-weight:300;
        ">
        Explore the Genome Within
        </h2>

        <p style="
        color:#DDE7FF;
        font-size:22px;
        ">
        Population Genomics Intelligence Platform
        </p>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div style='text-align:center;padding-top:40px;'>

        <div style='
        font-size:160px;
        filter:drop-shadow(0px 0px 30px #6AA8FF);
        '>
        🌙
        </div>

        </div>
        """, unsafe_allow_html=True)

    with st.container(border=True):

        st.markdown("""
            ## 🌌 Welcome to GeneVault

            Discover mutation hotspots, population genomic trends,
            and AI-powered healthcare insights using advanced analytics.

            🚀 Real-time Genomic Analytics  
            🧬 Population Research Dashboard  
            📊 Mutation Distribution Tracking  
            🤖 AI Assisted Research Insights
            """)
    db = get_db()

    collection = db["patients"]

    pipeline = [
        {"$unwind":"$mutations"},
        {
            "$group":{
                "_id":"$mutations.chr",
                "mutation_count":{"$sum":1}
            }
        },
        {
            "$sort":{
                "mutation_count":-1
            }
        }
    ]

    results = list(collection.aggregate(pipeline))

    total_patients = collection.count_documents({})

    total_mutations = collection.aggregate([
        {"$unwind":"$mutations"},
        {"$count":"count"}
    ])

    total_mutations = list(total_mutations)

    if total_mutations:
        total_mutations = total_mutations[0]["count"]
    else:
        total_mutations = 0

    if results:

        chart_data = pd.DataFrame(results)
        

        chart_data.columns = [
            "Chromosome",
            "Total Mutations"
        ]
        
        unique_chr = chart_data["Chromosome"].nunique()

        with st.container(border=True):

            st.subheader("📊 Population Statistics")

            col1,col2,col3 = st.columns(3)

            with col1:
                st.metric("Patients", total_patients)

            with col2:
                st.metric("Mutations", total_mutations)

            with col3:
                st.metric("Chromosomes", unique_chr)

        top_chr = chart_data.iloc[0]

        summary1, summary2, summary3 = st.columns(3)

        with summary1:
            st.metric(
                "Most Active Chromosome",
                top_chr["Chromosome"]
            )

        with summary2:
            st.metric(
                "Top Mutation Count",
                top_chr["Total Mutations"]
            )

        with summary3:
            st.metric(
                "Analysis Status",
                "Active"
            )

        col1,col2 = st.columns(2)

        with col1:
            st.info(
                f"""
        🔥 Most Active Chromosome

        Chromosome {top_chr['Chromosome']}

        {top_chr['Total Mutations']} Mutations
        """
            )

        with col2:
            st.success(
                """
        🧠 AI Insight

        Mutation activity indicates
        significant clustering in one
        chromosome region.
        """
            )


        with st.container(border=True):

            st.subheader("📈 Mutation Distribution")

            fig = px.bar(
                chart_data,
                x="Chromosome",
                y="Total Mutations"
            )   

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                height=500
            )

            st.plotly_chart(
            fig,
            use_container_width=True
            )

        with st.container(border=True):

            st.subheader("🥧 Chromosome Share")

            pie = px.pie(
                chart_data,
                values="Total Mutations",
                names="Chromosome"
            )

            pie.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                height=500
            )

            st.plotly_chart(
                pie,
                use_container_width=True
            )
        


        with st.container(border=True):

            st.subheader("🧬 Chromosome Database")

            st.dataframe(
                chart_data,
                use_container_width=True,
                hide_index=True
            )


        with st.container(border=True):

            st.subheader("🧠 AI Research Insight")

            st.write(
                f"""
        Chromosome {top_chr['Chromosome']}
        currently shows the highest mutation frequency.

        Researchers should prioritize
        further genomic investigation.
        """
            )

        with st.container(border=True):

            st.subheader("⚠ High Risk Chromosomes")

            high_risk = chart_data[
                chart_data["Total Mutations"] > 1
            ]

            st.dataframe(
                high_risk,
                use_container_width=True
            )

        st.markdown("""
        <br><br>

        <div style='
        text-align:center;
        color:#D6E4FF;
        font-size:18px;
        '>
        🧬 GeneVault Research Analytics Platform
        </div>
        """,
        unsafe_allow_html=True)

    else:
        st.warning("No Data Found")