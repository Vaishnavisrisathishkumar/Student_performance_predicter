// ============================================================
//  EduPredict AI — Frontend Script
// ============================================================

// ── Sync sliders ↔ inputs ───────────────────────────────────
function linkSlider(inputId, sliderId) {
  const input  = document.getElementById(inputId);
  const slider = document.getElementById(sliderId);

  slider.value = input.value || slider.value;

  input.addEventListener("input",  () => { slider.value = input.value; });
  slider.addEventListener("input", () => { input.value  = slider.value; });
}

document.addEventListener("DOMContentLoaded", () => {
  linkSlider("study_hours",    "study_slider");
  linkSlider("attendance",     "attendance_slider");
  linkSlider("previous_marks", "prev_slider");

  // Set initial values
  document.getElementById("study_hours").value    = 6;
  document.getElementById("attendance").value     = 85;
  document.getElementById("previous_marks").value = 72;
  document.getElementById("study_slider").value   = 6;
  document.getElementById("attendance_slider").value = 85;
  document.getElementById("prev_slider").value    = 72;
});


// ── Prediction ───────────────────────────────────────────────
async function predict() {
  const studyHours    = parseFloat(document.getElementById("study_hours").value);
  const attendance    = parseFloat(document.getElementById("attendance").value);
  const previousMarks = parseFloat(document.getElementById("previous_marks").value);
  const errorEl       = document.getElementById("error-msg");
  const btn           = document.getElementById("predictBtn");
  const btnText       = btn.querySelector(".btn-text");
  const btnLoader     = btn.querySelector(".btn-loader");

  // Client-side validation
  errorEl.style.display = "none";
  if (isNaN(studyHours) || isNaN(attendance) || isNaN(previousMarks)) {
    showError("Please fill in all three fields."); return;
  }
  if (studyHours < 0 || studyHours > 24) {
    showError("Study hours must be between 0 and 24."); return;
  }
  if (attendance < 0 || attendance > 100) {
    showError("Attendance must be between 0 and 100."); return;
  }
  if (previousMarks < 0 || previousMarks > 100) {
    showError("Previous marks must be between 0 and 100."); return;
  }

  // Loading state
  btn.disabled = true;
  btnText.style.display  = "none";
  btnLoader.style.display = "inline-flex";

  try {
    const res  = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        study_hours:    studyHours,
        attendance:     attendance,
        previous_marks: previousMarks,
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      showError(data.error || "Prediction failed. Please try again."); return;
    }

    displayResult(data);

  } catch (err) {
    showError("Network error. Please check your connection.");
  } finally {
    btn.disabled = false;
    btnText.style.display  = "inline-flex";
    btnLoader.style.display = "none";
  }
}


// ── Display result ───────────────────────────────────────────
function displayResult(data) {
  const resultCard = document.getElementById("resultCard");
  const scoreEl    = document.getElementById("scoreNum");
  const ringFill   = document.getElementById("ringFill");
  const gradeBadge = document.getElementById("gradeBadge");
  const gradeLabel = document.getElementById("gradeLabel");

  // Populate breakdown
  document.getElementById("res-study").textContent      = data.inputs.study_hours;
  document.getElementById("res-attendance").textContent = data.inputs.attendance + "%";
  document.getElementById("res-prev").textContent       = data.inputs.previous_marks;

  // Show card
  resultCard.style.display = "flex";
  resultCard.scrollIntoView({ behavior: "smooth", block: "center" });

  // Animate score counter
  animateCounter(scoreEl, 0, data.predicted_marks, 1200);

  // Animate ring (circumference = 2π×52 ≈ 326.73)
  const circumference = 326.73;
  const offset = circumference - (data.predicted_marks / 100) * circumference;
  setTimeout(() => {
    ringFill.style.strokeDashoffset = offset;
    ringFill.style.stroke = data.color;
  }, 100);

  // Grade
  gradeBadge.textContent = data.grade;
  gradeBadge.style.color = data.color;
  gradeBadge.style.borderColor = data.color;
  gradeLabel.textContent = data.label;
}


// ── Animate counter ──────────────────────────────────────────
function animateCounter(el, from, to, duration) {
  const start = performance.now();
  function step(now) {
    const elapsed  = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased    = 1 - Math.pow(1 - progress, 3);     // ease-out cubic
    el.textContent = (from + (to - from) * eased).toFixed(1);
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}


// ── Reset form ───────────────────────────────────────────────
function resetForm() {
  document.getElementById("resultCard").style.display = "none";
  document.getElementById("study_hours").value    = "";
  document.getElementById("attendance").value     = "";
  document.getElementById("previous_marks").value = "";
  document.getElementById("study_slider").value   = 6;
  document.getElementById("attendance_slider").value = 85;
  document.getElementById("prev_slider").value    = 72;

  // Reset ring
  document.getElementById("ringFill").style.strokeDashoffset = 326.73;

  window.scrollTo({ top: document.getElementById("predictor").offsetTop - 80, behavior: "smooth" });
}


// ── Show error ───────────────────────────────────────────────
function showError(msg) {
  const el = document.getElementById("error-msg");
  el.textContent    = "⚠ " + msg;
  el.style.display  = "block";

  const btn     = document.getElementById("predictBtn");
  const btnText = btn.querySelector(".btn-text");
  const loader  = btn.querySelector(".btn-loader");
  btn.disabled          = false;
  btnText.style.display = "inline-flex";
  loader.style.display  = "none";
}


// ── Enter key support ────────────────────────────────────────
document.addEventListener("keydown", (e) => {
  if (e.key === "Enter") predict();
});