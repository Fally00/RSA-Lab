const auditButton = document.querySelector("#auditButton");
const modulusInput = document.querySelector("#modulusInput");
const exponentInput = document.querySelector("#exponentInput");
const resultBox = document.querySelector(".result-box");
const stepsBox = document.querySelector(".steps-box");

function addStep(title, result) {
    const step = document.createElement("div");
    step.className = "check-step";
    const heading = document.createElement("span");
    heading.className = "check-step-title";
    heading.textContent = title;
    const detail = document.createElement("div");
    detail.className = "check-step-result";
    detail.textContent = result;
    step.append(heading, detail);
    stepsBox.append(step);
}

auditButton.addEventListener("click", async () => {
    const n = modulusInput.value.trim();
    const e = exponentInput.value.trim();
    if (!n || !e) return;

    auditButton.disabled = true;
    try {
        const response = await fetch("/api/audit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input: `${n}, ${e}` })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Audit failed.");

        const key = data.keys[0];
        const results = key.results || [];
        const broken = results.find((item) => item.broken);
        const verdict = resultBox.querySelector(".result-result span");
        const summary = resultBox.querySelector(".result-result p");
        const details = resultBox.querySelectorAll(".result-details span");
        resultBox.querySelector(".result-title-box span").textContent = `${key.bits}-BIT MODULUS`;
        verdict.textContent = key.verdict === "BROKEN" ? "WEAK KEY" : "NO WEAKNESS FOUND";
        summary.textContent = broken
            ? `${broken.attack} recovered factors ${broken.factors.join(" × ")}.`
            : "No registered attack recovered this key.";
        details[0].textContent = `${key.bits} bits`;
        details[1].textContent = `e = ${key.e}`;
        details[2].textContent = broken ? `p = ${broken.factors.join(", q = ")}` : "Not factored";
        details[3].textContent = broken?.private_key || "Not recovered";

        stepsBox.querySelectorAll(".check-step").forEach((step) => step.remove());
        results.forEach((item) => {
            addStep(`${item.attack} · ${item.broken ? "BROKEN" : "SAFE"}`,
                (item.steps || []).map((line) => typeof line === "string" ? line : "Table of diagnostic values").join(" "));
        });
        stepsBox.querySelector(".steps-box-title-box span:last-child").textContent = `${results.length} ATTACKS RUN`;
    } catch (error) {
        resultBox.querySelector(".result-result p").textContent = error.message;
    } finally {
        auditButton.disabled = false;
    }
});
