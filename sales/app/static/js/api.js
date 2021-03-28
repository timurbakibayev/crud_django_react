const login_api = async (username, password, success, fail) => {
  const response = await fetch(
        `/api/token/`,
        {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              "username": username,
              "password": password,
            })
        }
    );
  const text = await response.text();
  if (response.status === 200) {
    console.log("success", JSON.parse(text));
    success(text);
  } else {
    console.log("failed", text);
    fail(text);
  }
};