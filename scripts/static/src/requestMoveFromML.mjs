import { llama } from '../libs/llamacpp.mjs';

export async function requestMoveFromML(prompt) {
  const baseUrl = '/proxy';
  console.log('Requesting ML Move');
  // let responseText = '';
  // const request = llama(prompt, { n_predict: 800 }, { baseURL: baseUrl })
  // for await (const chunk of request) {
  //   console.log(chunk.data.content)
  //   responseText += chunk.data.content;
  // }
  // console.log('responseText', responseText);

  console.group('Health Check');
  let response = await fetch('api/health');
  console.log('response', response);
  let data = await response.json();
  console.log('data', data);
  console.groupEnd();

  console.group('Request Move');
  response = await fetch('api/completion', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 
      prompt: prompt,
      // temperature: 0.5,
      // max_tokens: 800,
      // top_p: 1,
      // frequency_penalty: 0,
      // presence_penalty: 0,
    }),
  });
  console.log('response', response);
  data = await response.json();
  console.log('data', data);
  console.groupEnd();

  return data.content;
}