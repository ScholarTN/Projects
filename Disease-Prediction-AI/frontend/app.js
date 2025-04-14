// Add these debug logs at the top of your app.js file
console.log("App initializing...");

// Chart variables at the top
let riskChart = null;
let doctorChart = null;

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded");
  
  // DOM Elements
  const roleSelection = document.getElementById("role-selection");
  const loginForm = document.getElementById("login-form");
  const registerRoleSelection = document.getElementById("register-role-selection");
  const registerPatientForm = document.getElementById("register-patient-form");
  const registerDoctorForm = document.getElementById("register-doctor-form");
  const userDashboard = document.getElementById("user-dashboard");
  const doctorDashboard = document.getElementById("doctor-dashboard");
  const selectUserBtn = document.getElementById("select-user");
  const selectDoctorBtn = document.getElementById("select-doctor");
  const showRegisterBtn = document.getElementById("show-register");
  const registerShowLoginBtns = document.querySelectorAll("#register-show-login");
  const loginWorkIdField = document.getElementById("login-workid-field");
  const predictForm = document.getElementById("predict-form");
  const resultContainer = document.getElementById("result");
  const suggestionBox = document.getElementById("suggestion");
  const userLogsContainer = document.getElementById("user-logs");
  const userLogoutBtn = document.getElementById("user-logout");
  const doctorLogoutBtn = document.getElementById("doctor-logout");
  const recordsList = document.getElementById("records-list");
  const totalPatientsEl = document.getElementById("total-patients");
  const highRiskCasesEl = document.getElementById("high-risk-cases");
  const downloadCSV = document.getElementById("download-csv");
  const downloadPDF = document.getElementById("download-pdf");

  // App State
  let currentToken = null;
  let currentRole = null;
  let currentEmail = null;

  // Debug element existence
  console.log("User dashboard exists:", !!userDashboard);
  console.log("Login form exists:", !!loginForm);
  console.log("Predict form exists:", !!predictForm);

  // Initialize
  initCharts();

  // Event Listeners
  selectUserBtn.addEventListener("click", () => {
    console.log("User role selected");
    currentRole = "user";
    roleSelection.style.display = "none";
    loginForm.style.display = "block";
    
    // Remove required attribute from work ID field for patients
    const workIdInput = document.getElementById("login-workid");
    workIdInput.required = false;
    loginWorkIdField.style.display = "none";
  });

  selectDoctorBtn.addEventListener("click", () => {
    console.log("Doctor role selected");
    currentRole = "doctor";
    roleSelection.style.display = "none";
    loginForm.style.display = "block";
    
    // Set required attribute for work ID field for doctors
    const workIdInput = document.getElementById("login-workid");
    workIdInput.required = true;
    loginWorkIdField.style.display = "block";
  });

  // Show register role selection when "Register here" is clicked
  showRegisterBtn.addEventListener("click", (e) => {
    e.preventDefault();
    loginForm.style.display = "none";
    registerRoleSelection.style.display = "block";
  });

  // Register Role Selection
  document.getElementById("register-select-user").addEventListener("click", () => {
    currentRole = "user";
    registerRoleSelection.style.display = "none";
    registerPatientForm.style.display = "block";
  });

  document.getElementById("register-select-doctor").addEventListener("click", () => {
    currentRole = "doctor";
    registerRoleSelection.style.display = "none";
    registerDoctorForm.style.display = "block";
  });

  // Register Patient
  document.getElementById("register-patient-form-data").addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("register-patient-email").value;
    const password = document.getElementById("register-patient-password").value;

    const submitBtn = e.target.querySelector("button[type='submit']");
    submitBtn.disabled = true;
    submitBtn.querySelector("span").textContent = "Registering...";

    try {
      const res = await fetch("http://127.0.0.1:5050/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          email, 
          password, 
          role: "user"
        }),
      });
      const data = await res.json();
      alert(data.message);
      if (data.status === "success") {
        registerPatientForm.style.display = "none";
        loginForm.style.display = "block";
        e.target.reset();
      }
    } catch (error) {
      console.error("Registration error:", error);
      alert("Registration failed. Please try again.");
    } finally {
      submitBtn.disabled = false;
      submitBtn.querySelector("span").textContent = "Register";
    }
  });

  // Register Doctor
  document.getElementById("register-doctor-form-data").addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("register-doctor-email").value;
    const password = document.getElementById("register-doctor-password").value;
    const workId = document.getElementById("register-doctor-workid").value;

    const submitBtn = e.target.querySelector("button[type='submit']");
    submitBtn.disabled = true;
    submitBtn.querySelector("span").textContent = "Registering...";

    try {
      const res = await fetch("http://127.0.0.1:5050/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          email, 
          password, 
          role: "doctor",
          workId
        }),
      });
      const data = await res.json();
      alert(data.message);
      if (data.status === "success") {
        // Reset forms and show doctor login
        e.target.reset();
        document.getElementById("register-doctor-form").style.display = "none";
        document.getElementById("login-form").style.display = "block";
        // Set role to doctor and show work ID field
        currentRole = "doctor";
        document.getElementById("login-workid-field").style.display = "block";
      }
    } catch (error) {
      console.error("Registration error:", error);
      alert("Registration failed. Please try again.");
    } finally {
      submitBtn.disabled = false;
      submitBtn.querySelector("span").textContent = "Register";
    }
  });

  // Toggle back to login from register forms
  registerShowLoginBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      registerRoleSelection.style.display = "none";
      registerPatientForm.style.display = "none";
      registerDoctorForm.style.display = "none";
      loginForm.style.display = "block";
    });
  });

  // Fix the login form submission handler
document.getElementById("login-form-data").addEventListener("submit", async (e) => {
  e.preventDefault();
  console.log("Login form submitted");

  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;
  
  // Only get workId if it's a doctor login and the field is visible
  const workId = currentRole === "doctor" ? document.getElementById("login-workid").value : null;

  console.log("Attempting login with:", { email, role: currentRole, hasWorkId: !!workId });

  const submitBtn = e.target.querySelector("button[type='submit']");
  submitBtn.disabled = true;
  submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';

  try {
    // Debug point
    console.log("About to send login request to backend");
    
    const requestBody = {
      email,
      password,
      role: currentRole
    };
    
    // Only add workId for doctor role
    if (currentRole === "doctor") {
      requestBody.workId = workId;
    }
    
    console.log("Request payload:", requestBody);
    
    const response = await fetch("http://127.0.0.1:5050/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });

    console.log("Login response status:", response.status);
    const data = await response.json();
    console.log("Login response data:", data);

    if (data.status === "success") {
      // Store user information
      currentToken = data.token;
      currentRole = data.role;
      currentEmail = data.email;
      
      console.log("Login successful for role:", currentRole);
      
      // Save token to sessionStorage for persistence
      sessionStorage.setItem('userToken', currentToken);
      sessionStorage.setItem('userRole', currentRole);
      sessionStorage.setItem('userEmail', currentEmail);

      // Hide all auth sections
      roleSelection.style.display = "none";
      loginForm.style.display = "none";
      registerRoleSelection.style.display = "none";
      registerPatientForm.style.display = "none";
      registerDoctorForm.style.display = "none";

      // Show appropriate dashboard based on role
      if (currentRole === "user") {
        console.log("Showing user dashboard");
        userDashboard.style.display = "block";
        doctorDashboard.style.display = "none";
        
        // Reset form and hide previous results
        if (predictForm) {
          predictForm.reset();
          resultContainer.style.display = "none";
        }
        
        // Load user history
        loadUserLogs();
      } else if (currentRole === "doctor") {
        console.log("Showing doctor dashboard");
        userDashboard.style.display = "none";
        doctorDashboard.style.display = "block";
        loadDoctorData();
      } else {
        console.warn("Unknown role:", currentRole);
        alert("Unknown user role. Please contact support.");
      }
    } else {
      console.error("Login failed:", data.message);
      alert(data.message || "Login failed");
    }
  } catch (error) {
    console.error("Login error:", error);
    alert("Login failed. Please try again. Error: " + error.message);
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<span>Login</span><i class="fas fa-arrow-right"></i>';
  }
});

  // Logout
  function logout() {
    console.log("Logging out");
    currentToken = null;
    currentRole = null;
    currentEmail = null;
    
    // Hide all sections
    userDashboard.style.display = "none";
    doctorDashboard.style.display = "none";
    loginForm.style.display = "none";
    registerRoleSelection.style.display = "none";
    registerPatientForm.style.display = "none";
    registerDoctorForm.style.display = "none";
    
    // Show role selection
    roleSelection.style.display = "block";
    
    // Reset forms
    predictForm.reset();
    document.getElementById("login-form-data").reset();
    document.getElementById("register-patient-form-data").reset();
    document.getElementById("register-doctor-form-data").reset();
    
    // Hide work ID field
    loginWorkIdField.style.display = "none";
    
    resultContainer.style.display = "none";
  }

  userLogoutBtn.addEventListener("click", logout);
  doctorLogoutBtn.addEventListener("click", logout);

  // Predict
  predictForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log("Prediction form submitted");
    
    // Get all form values
    const formData = {
      age: document.getElementById("age").value,
      gender: document.getElementById("gender").value,
      is_pregnant: document.getElementById("is_pregnant") ? document.getElementById("is_pregnant").value : 0,
      height: document.getElementById("height").value || 0,
      weight: document.getElementById("weight").value || 0,
      bmi: document.getElementById("bmi").value || 0,
      glucose: document.getElementById("glucose").value,
      blood_pressure: document.getElementById("blood_pressure").value,
      family_history: document.getElementById("family_history").value
    };

    // Validate required fields
    if (!formData.age || !formData.glucose || !formData.blood_pressure || !formData.family_history || !formData.gender) {
      alert("Please fill in all required fields");
      return;
    }

    const submitBtn = e.target.querySelector("button[type='submit']");
    submitBtn.disabled = true;
    submitBtn.textContent = "Analyzing...";

    try {
      const res = await fetch("http://127.0.0.1:5050/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          token: currentToken,
          ...formData
        }),
      });

      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.message || "Prediction failed");
      }

      if (data.status === "success") {
        updateRiskChart(data.risk_score, data.prediction);
        showSuggestion(data.prediction, data.suggestion);
        loadUserLogs();
        document.getElementById("result").style.display = "block";
      } else {
        alert(data.message || "Prediction failed");
      }
    } catch (error) {
      console.error("Prediction error:", error);
      alert(error.message || "Prediction failed. Please try again.");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Check Risk";
    }
  });

  // Download Reports
  downloadCSV?.addEventListener("click", () => downloadReport("csv"));
  downloadPDF?.addEventListener("click", () => downloadReport("pdf"));

  async function loadUserLogs() {
    try {
      console.log("Loading user logs with token:", currentToken);
      const res = await fetch(`http://127.0.0.1:5050/logs?token=${currentToken}`);
      const data = await res.json();

      if (data.status === "success" && data.logs.length > 0) {
        userLogsContainer.innerHTML = "<h3>Your History</h3>";
        data.logs.forEach(log => {
          userLogsContainer.innerHTML += `
            <div class="log-entry">
              <p><strong>Date:</strong> ${new Date(log.timestamp).toLocaleString()}</p>
              <p class="${log.prediction === 1 ? 'high-risk' : 'low-risk'}">
                <strong>Result:</strong> ${log.prediction === 1 ? "High Risk" : "Low Risk"}
              </p>
            </div>
          `;
        });
      }
    } catch (error) {
      console.error("Failed to load logs:", error);
    }
  }

  async function loadDoctorData() {
    try {
      // Load summary stats
      const summaryRes = await fetch(`http://127.0.0.1:5050/admin-summary?token=${currentToken}`);
      const summaryData = await summaryRes.json();

      if (summaryData.status === "success") {
        totalPatientsEl.textContent = summaryData.summary.total_users;
        highRiskCasesEl.textContent = summaryData.summary.diabetic_cases;
        updateDoctorChart(summaryData.summary);
      }

      // Load patient records
      const recordsRes = await fetch(`http://127.0.0.1:5050/all-records?token=${currentToken}`);
      const recordsData = await recordsRes.json();

      if (recordsData.status === "success" && recordsData.records.length > 0) {
        recordsList.innerHTML = "";
        recordsData.records.forEach(record => {
          recordsList.innerHTML += `
            <div class="record-item">
              <p><strong>Patient:</strong> ${record.email}</p>
              <p><strong>Date:</strong> ${new Date(record.timestamp).toLocaleString()}</p>
              <p class="${record.prediction === 1 ? 'high-risk' : 'low-risk'}">
                <strong>Risk:</strong> ${record.prediction === 1 ? "High" : "Low"}
              </p>
              <p><strong>Glucose:</strong> ${record.glucose} mg/dL</p>
              <p><strong>BMI:</strong> ${record.bmi}</p>
            </div>
          `;
        });
      }
    } catch (error) {
      console.error("Failed to load doctor data:", error);
    }
  }

  async function downloadReport(type) {
    try {
      const btn = type === 'csv' ? downloadCSV : downloadPDF;
      const originalContent = btn.innerHTML;
      btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
      btn.disabled = true;

      const response = await fetch(`http://127.0.0.1:5050/download?token=${currentToken}&type=${type}`);
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to generate report');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = `diabetes_records.${type}`;
      document.body.appendChild(a);
      a.click();
      
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

    } catch (error) {
      console.error('Download error:', error);
      alert(`Download failed: ${error.message}`);
    } finally {
      const btn = type === 'csv' ? downloadCSV : downloadPDF;
      btn.innerHTML = originalContent;
      btn.disabled = false;
    }
  }

  function initCharts() {
    try {
      console.log("Initializing charts");
      
      // Risk Chart (Donut)
      const riskCtx = document.getElementById('riskChart')?.getContext('2d');
      if (riskCtx) {
        riskChart = new Chart(riskCtx, {
          type: 'doughnut',
          data: {
            labels: ['Low Risk', 'High Risk'],
            datasets: [{
              data: [1, 0],
              backgroundColor: ['#388e3c', '#d32f2f'],
              borderWidth: 0
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'bottom'
              }
            },
            cutout: '70%'
          }
        });
      } else {
        console.warn("Risk chart canvas not found");
      }

      // Doctor Chart (Donut)
      const doctorCtx = document.getElementById('doctorChart')?.getContext('2d');
      if (doctorCtx) {
        doctorChart = new Chart(doctorCtx, {
          type: 'doughnut',
          data: {
            labels: ['Low Risk', 'High Risk'],
            datasets: [{
              data: [1, 0],
              backgroundColor: ['#388e3c', '#d32f2f'],
              borderWidth: 0
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'bottom'
              },
              title: {
                display: true,
                text: 'Patient Risk Distribution',
                font: {
                  size: 16
                }
              }
            },
            cutout: '60%'
          }
        });
      } else {
        console.warn("Doctor chart canvas not found");
      }
    } catch (error) {
      console.error("Chart initialization error:", error);
    }
  }

  function updateRiskChart(riskScore, riskLevel) {
    try {
      let colors = [];
      if (riskLevel === "very high") {
        colors = ['#d32f2f', '#e0e0e0'];
      } else if (riskLevel === "high") {
        colors = ['#ffa000', '#e0e0e0'];
      } else if (riskLevel === "medium") {
        colors = ['#ffc107', '#e0e0e0'];
      } else {
        colors = ['#388e3c', '#e0e0e0'];
      }

      if (riskChart) {
        riskChart.destroy();
      }

      const ctx = document.getElementById('riskChart').getContext('2d');
      riskChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Risk', 'Remaining'],
          datasets: [{
            data: [riskScore, 100-riskScore],
            backgroundColor: colors,
            borderWidth: 0
          }]
        },
        options: {
          cutout: '70%',
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `${context.label}: ${context.raw}%`;
                }
              }
            }
          },
          animation: {
            animateScale: true,
            animateRotate: true
          }
        }
      });
    } catch (error) {
      console.error("Risk chart update error:", error);
    }
  }

  function updateDoctorChart(summary) {
    try {
      if (doctorChart) {
        doctorChart.data.datasets[0].data = [
          summary.non_diabetic_cases,
          summary.diabetic_cases
        ];
        doctorChart.update();
      }
    } catch (error) {
      console.error("Doctor chart update error:", error);
    }
  }

  function showSuggestion(prediction, suggestion) {
    try {
      suggestionBox.innerHTML = `
        <h4>${prediction === "very high" || prediction === "high" ? "High Risk Detected" : "Low Risk"}</h4>
        <p>${suggestion}</p>
        ${prediction === "very high" || prediction === "high" ? `
          <ul class="suggestion-list">
            <li><i class="fas fa-utensils"></i> Reduce sugar and refined carbs intake</li>
            <li><i class="fas fa-dumbbell"></i> Exercise regularly (30 mins/day)</li>
            <li><i class="fas fa-weight"></i> Maintain healthy weight</li>
            <li><i class="fas fa-user-md"></i> Consult your doctor for regular checkups</li>
          </ul>
        ` : `
          <p>Keep maintaining your healthy lifestyle!</p>
        `}
      `;
    } catch (error) {
      console.error("Suggestion display error:", error);
    }
  }

  // Show/hide pregnancy field based on gender
  document.getElementById('gender')?.addEventListener('change', function() {
    const pregnancyField = document.getElementById('pregnancy-field');
    if (pregnancyField) {
      pregnancyField.style.display = this.value === 'female' ? 'block' : 'none';
    }
  });

  // Add medical standard placeholders
  const medicalStandards = {
    bmi: "Normal: 18.5-24.9 | Overweight: 25-29.9 | Obese: ≥30",
    glucose: "Normal: <100 mg/dL | Prediabetic: 100-125 | Diabetic: ≥126",
    blood_pressure: "Normal: <120/80 | Elevated: 120-129/<80 | High: ≥130/80"
  };

  // Set placeholders on focus
  Object.keys(medicalStandards).forEach(id => {
    const field = document.getElementById(id);
    if (field) {
      field.addEventListener('focus', () => {
        field.placeholder = medicalStandards[id];
        field.style.borderColor = '#1976d2';
      });
      field.addEventListener('blur', () => {
        field.style.borderColor = '';
      });
    }
  });

  // Calculate BMI if height/weight provided
  function calculateBMI() {
    const height = parseFloat(document.getElementById('height')?.value) / 100;
    const weight = parseFloat(document.getElementById('weight')?.value);
    
    if (height && weight) {
      const bmi = weight / (height * height);
      const bmiField = document.getElementById('bmi');
      if (bmiField) {
        bmiField.value = bmi.toFixed(1);
        updateBMIGuidance();
      }
    }
  }

  // Update BMI guidance based on age
  function updateBMIGuidance() {
    const age = parseInt(document.getElementById('age')?.value);
    const bmiField = document.getElementById('bmi');
    
    if (age && bmiField) {
      let normalRange;
      if (age < 18) {
        normalRange = "BMI ranges for children are age-specific";
      } else if (age < 65) {
        normalRange = "Normal: 18.5-24.9 | Overweight: 25-29.9 | Obese: ≥30";
      } else {
        normalRange = "Normal: 23-27 (slightly higher for seniors)";
      }
      bmiField.placeholder = `For age ${age}: ${normalRange}`;
    }
  }

  // Event listeners
  document.getElementById('height')?.addEventListener('input', calculateBMI);
  document.getElementById('weight')?.addEventListener('input', calculateBMI);
  document.getElementById('age')?.addEventListener('input', updateBMIGuidance);
  
  const genderField = document.getElementById('gender');
  const pregnancyField = document.getElementById('pregnancy-field');
  
  if (genderField && pregnancyField) {
    genderField.addEventListener('change', function() {
      pregnancyField.style.display = this.value === 'female' ? 'block' : 'none';
    });
  }
});
