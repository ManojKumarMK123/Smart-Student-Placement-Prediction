import streamlit as st
import numpy as np
import joblib  # To load the trained model

# Load the trained model
model = joblib.load("random_forest.pkl")  # Change filename if different

# Streamlit UI
st.title("🎓 Student Placement Prediction")

st.markdown("Enter student details to predict placement status and probability.")

# Input fields
CGPA = st.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1)
Internships = st.number_input("Number of Internships", min_value=0, step=1)
Projects = st.number_input("Number of Projects", min_value=0, step=1)
Certifications = st.number_input("Number of Certifications", min_value=0, step=1)
AptitudeTestScore = st.number_input("Aptitude Test Score (out of 100)", min_value=0.0, max_value=100.0, step=0.1)
SoftSkillsRating = st.number_input("Soft Skills Rating (out of 5)", min_value=0.0, max_value=5.0, step=0.1)
ExtracurricularActivities = st.radio("Extracurricular Activities", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
PlacementTraining = st.radio("Placement Training Attended", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
SSC_Marks = st.number_input("SSC Marks (%)", min_value=0.0, max_value=100.0, step=0.1)
HSC_Marks = st.number_input("HSC Marks (%)", min_value=0.0, max_value=100.0, step=0.1)

# Prediction button
def Predictor(CGPA,Internships, Projects, Certifications, AptitudeTestScore, SoftSkillsRating, ExtracurricularActivities, 
PlacementTraining, SSC_Marks, HSC_Marks):
    probability = 0
    if(CGPA>7.6):
        probability+=(CGPA/100)
    if (AptitudeTestScore>75):
        probability+=(AptitudeTestScore/1000)
    if SoftSkillsRating>4:
        probability+=(SoftSkillsRating*2/100)
    if Projects>3:
        probability+=(0.1)
    elif Projects==2:
        probability+=0.08
    elif Projects==1:
        probability+=0.05
    if Certifications>3:
        probability+=(0.1)
    elif Certifications==2:
        probability+=0.08
    elif Certifications==1:
        probability+=0.05
    if Internships>2:
        probability+=(0.1)
    elif Internships==2:
        probability+=0.07
    elif Internships==1:
        probability+=0.05
    if ExtracurricularActivities=='Yes' or ExtracurricularActivities==1:
        probability+=0.1
    if PlacementTraining=='Yes' or PlacementTraining==1:
        probability+=0.1
    probability+=(HSC_Marks/1000)
    probability+=(SSC_Marks/1000)
    if probability>0.7:
        return [True,probability]
    else:
        return [False,probability]


if st.button("Predict Placement"):
    # Prepare input array
    input_data = np.array([[CGPA, Internships, Projects, Certifications, 
                            AptitudeTestScore, SoftSkillsRating, ExtracurricularActivities, 
                            PlacementTraining, SSC_Marks, HSC_Marks]])

    # Predict placement
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1] * 100  # Probability of placement
    ans = Predictor(CGPA, Internships, Projects, Certifications, 
                            AptitudeTestScore, SoftSkillsRating, ExtracurricularActivities, 
                            PlacementTraining, SSC_Marks, HSC_Marks)
    if ans[0]==True:
        st.subheader(f"Prediction: ✅ Placed")
        st.metric(label="Placement Probability", value=f"{(ans[1]*100):.2f} %")
    else:
        st.metric(label="Placement Probability", value="❌ Not Placed")
        print("❌ Not Placed",ans[1])
    # Display result
    # placement_status = "✅ Placed" if prediction == 1 else "❌ Not Placed"
    # st.subheader(f"Prediction: {placement_status}")
    # st.metric(label="Placement Probability", value=f"{probability:.2f} %")
