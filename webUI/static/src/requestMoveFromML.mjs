
export async function requestMoveFromML(prompt) {
  const response = await fetch('api/completion', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 
      prompt: prompt,
      n_keep: 35,
    }),
  });
  const data = await response.json();
  return data.content;
}