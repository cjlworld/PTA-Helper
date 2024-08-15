console.log("Content script loaded");

// 引入 marked 库
const script = document.createElement('script');
script.src = "https://cdn.jsdelivr.net/npm/marked/marked.min.js";
script.onload = () => {
  console.log("marked library loaded");
  init();
};
document.head.appendChild(script);

// sleep
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 等待页面加载完成
async function waitForPageLoad() {
  return sleep(10000);
}

const BASE_URL = "http://localhost:8080";

// 定义一个函数来处理流响应
async function handleStreamResponse(blockHtml, outputElement) {
  console.log("blockHtml:", blockHtml);
  // 使用 fetch 获取流响应
  const response = await fetch(BASE_URL + "/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ description: blockHtml })
    });

  // 检查响应是否是流
  if (!response.body) {
    throw new Error('Response does not contain a ReadableStream');
  }

  // 获取 ReadableStream
  const reader = response.body.getReader();

  // 创建一个用于显示所有数据的 <div> 元素
  const divElement = document.createElement('div');
  outputElement.appendChild(divElement);

  // 定义一个变量来存储累积的文本
  let accumulatedText = '';

  // 定义一个异步函数来读取流数据
  async function readStream() {
    while (true) {
      // 读取流数据块
      const { done, value } = await reader.read();

      // 如果流读取完成，退出循环
      if (done) {
        break;
      }

      // 处理数据块（例如，将 Uint8Array 转换为字符串）
      const chunk = new TextDecoder("utf-8").decode(value);

      // 将数据块追加到 accumulatedText
      accumulatedText += chunk;
      
      // // 将数据块追加到 <p> 元素中
      // pElement.textContent += chunk;

      // 将 accumulatedText 作为 Markdown 转换为 HTML
      const htmlContent = marked.parse(accumulatedText);

      // 用转换后的 HTML 替换 divElement 的内容
      divElement.innerHTML = htmlContent;

      // 确保页面滚动到最新数据的位置
      outputElement.scrollTop = outputElement.scrollHeight;
    }
  }

  // 开始读取流
  await readStream();
}

// 执行脚本
waitForPageLoad().then(() => {
  const problemBlocks = document.querySelectorAll("div.pc-x.pt-2.pl-4");

  console.log('Problem blocks:', problemBlocks);
  
  problemBlocks.forEach((block) => {
    const button = document.createElement("button");
    button.textContent = "Show Solution";
    button.classList.add("solution-button");
    block.appendChild(button);
  
    button.addEventListener("click", async function() {
      // alert("Solution button clicked!");
      // 将 当前 block 的 html 代码转换为 str
      const blockHtml = block.innerHTML;
      console.log(blockHtml);

      // 发送到后端
      await handleStreamResponse(blockHtml, block);
    });
  });  
})


