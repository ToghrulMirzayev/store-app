async function authenticateUser() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);
  formData.append("grant_type", "password");

  try {
    const response = await fetch("/auth/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    });

    if (!response.ok) {
      const errorMessageElement = document.getElementById("message");
      errorMessageElement.textContent = "Credentials are not valid";
      errorMessageElement.classList.add("error-message");
      return;
    }
    window.location.href = "/stores";
  } catch (error) {
    console.error("Error during authentication:", error);
  }
}
