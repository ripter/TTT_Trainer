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

  const response = await fetch(`${baseUrl}/health`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      // 'Authorization': 'Bearer abc123',
      // 'Sec-Fetch-Dest': 'empty',
      // 'Sec-Fetch-Mode': 'cors',
      // 'Sec-Fetch-Site': 'cross-site',
      // 'Access-Control-Allow-Origin': 'http://localhost:4400/',
      // 'Access-Control-Allow-Origin': '*',
    },
  });
  console.log('response', response);
  const data = await response.json();
  console.log('data', data);
}