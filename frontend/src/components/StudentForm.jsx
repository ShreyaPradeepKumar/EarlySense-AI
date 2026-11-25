/*
  StudentForm component displays input fields for student data.
  It receives data and handlers from App.jsx as props.
*/
function StudentForm({ formData, onChange, onSubmit, loading }) {
  return (
    <section className="card">
      <h2>Student Details</h2>
      <p className="card-subtitle">Enter student information to check early risk.</p>

      <form onSubmit={onSubmit} className="form">
        <label>
          Gender
          <select name="gender" value={formData.gender} onChange={onChange}>
            <option value="female">Female</option>
            <option value="male">Male</option>
          </select>
        </label>

        <label>
          Race/Ethnicity
          <select name="race/ethnicity" value={formData['race/ethnicity']} onChange={onChange}>
            <option value="group A">Group A</option>
            <option value="group B">Group B</option>
            <option value="group C">Group C</option>
            <option value="group D">Group D</option>
            <option value="group E">Group E</option>
          </select>
        </label>

        <label>
          Parental Level of Education
          <select
            name="parental level of education"
            value={formData['parental level of education']}
            onChange={onChange}
          >
            <option value="some high school">Some High School</option>
            <option value="high school">High School</option>
            <option value="some college">Some College</option>
            <option value="associate's degree">Associate's Degree</option>
            <option value="bachelor's degree">Bachelor's Degree</option>
            <option value="master's degree">Master's Degree</option>
          </select>
        </label>

        <label>
          Lunch
          <select name="lunch" value={formData.lunch} onChange={onChange}>
            <option value="standard">Standard</option>
            <option value="free/reduced">Free/Reduced</option>
          </select>
        </label>

        <label>
          Test Preparation Course
          <select
            name="test preparation course"
            value={formData['test preparation course']}
            onChange={onChange}
          >
            <option value="none">None</option>
            <option value="completed">Completed</option>
          </select>
        </label>

        <button type="submit" disabled={loading} className="submit-btn">
          {loading ? 'Predicting...' : 'Predict Risk'}
        </button>
      </form>
    </section>
  )
}

export default StudentForm
