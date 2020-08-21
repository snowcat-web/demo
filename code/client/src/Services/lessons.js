export const signupLesson = async (data) => {
  const response = await fetch(`/signup-lessson/`, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    data: data
  });
  if (!response.ok) {
    return null;
  }
  const responseData = await response.json();
  return responseData;
};