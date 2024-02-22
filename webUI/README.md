# Run UI

The Web UI can work with any ML server that follows the same format at llama.cpp's [server](https://github.com/ggerganov/llama.cpp/blob/master/examples/server/README.md).

It performs a POST `/completion` request with the prompt. It expects the response to be formatted like `{content: 'ml response text'}`.


```
python webUI/server.py 
```

