const sizeOptions = [12, 32, 64, 512, 1024];
let selectedBits = 1024;

const generateButton = document.querySelector("#generateButton");
const resetButton = document.querySelector("#generateResetButton");
const exponentInput = document.querySelector("#exponentInput");
const seedInput = document.querySelector("#seedInput");
const resultBox = document.querySelector(".result-box");
const stepsBox = document.querySelector(".steps-box");

sizeOptions.forEach((bits) => {
    const option = document.querySelector(`#bit${bits}`);
    option.addEventListener("click", () => {
        selectedBits = bits;
        document.querySelectorAll(".radios div").forEach((item) => item.classList.remove("active"));
        option.classList.add("active");
    });
});
document.querySelector("#bit1024").classList.add("active");

async function generateKey() {
    generateButton.disabled = true;
    resetButton.disabled = true;
    try {
        const response = await fetch("/api/keygen", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                bits: selectedBits,
                exponent: exponentInput.value.trim(),
                seed: seedInput.value.trim()
            })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Key generation failed.");

        const key = data.strong;
        resultBox.querySelector(".result-title-box span").textContent = `VALID · ${key.bits}-BIT RSA`;
        const keyValues = resultBox.querySelectorAll(".result-result p");
        keyValues[0].textContent = `(${key.n}, ${key.e})`;
        keyValues[1].textContent = `(${key.n}, ${key.d})`;
        const details = resultBox.querySelectorAll(".result-details span");
        details[0].textContent = `p = ${key.p}, q = ${key.q}`;
        details[1].textContent = key.n;
        details[2].textContent = "Generated from two distinct primes";
        details[3].textContent = key.phi;

        stepsBox.querySelectorAll(".step").forEach((step) => step.remove());
        key.steps.forEach((line, index) => {
            const step = document.createElement("div");
            step.className = "step";
            const title = document.createElement("span");
            title.className = "step-title";
            title.textContent = `STEP ${String(index + 1).padStart(2, "0")}`;
            const result = document.createElement("div");
            result.className = "step-result";
            result.textContent = line;
            step.append(title, result);
            stepsBox.append(step);
        });
        stepsBox.querySelector(".steps-box-title-box span:last-child").textContent = `${key.steps.length} STEPS`;
    } catch (error) {
        resultBox.querySelector(".result-result .public-key p").textContent = error.message;
    } finally {
        generateButton.disabled = false;
        resetButton.disabled = false;
    }
}

generateButton.addEventListener("click", generateKey);
resetButton.addEventListener("click", () => {
    seedInput.value = "";
    generateKey();
});
