console.log("Content script loaded");

// sleep
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 等待页面加载完成
async function waitForPageLoad() {
  return sleep(10000);
}

// 执行脚本
waitForPageLoad().then(() => {
  const problemBlocks = document.querySelectorAll("div.pc-v.pc-gap-12");

  console.log('Problem blocks:', problemBlocks);
  
  problemBlocks.forEach((block) => {
    const button = document.createElement("button");
    button.textContent = "Show Solution";
    button.classList.add("solution-button");
    block.appendChild(button);
  
    button.addEventListener("click", function () {
      alert("Solution button clicked!");
      // 在这里添加显示解析的逻辑
    });
  });  
})

