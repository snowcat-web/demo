export const signupLesson = async (data) => {
  const response = await fetch("/lessons", {
    method: "POST",
    headers: {
      "Accept": "*/*",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data)
  });
  const responseData = await response.json();
  return responseData;
};