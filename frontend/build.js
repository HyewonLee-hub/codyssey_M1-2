const fs = require("fs");
const path = require("path");


const distDir = path.join(__dirname, "dist");


// 기존 dist 삭제
fs.rmSync(distDir, {
  recursive: true,
  force: true
});


// 새 dist 생성
fs.mkdirSync(distDir, {
  recursive: true
});


// 정적 파일 복사
const files = [
  "index.html",
  "style.css",
  "script.js"
];

files.forEach((file) => {
  fs.copyFileSync(
    path.join(__dirname, file),
    path.join(distDir, file)
  );
});


// Vercel 환경변수 읽기
const apiBaseUrl =
  process.env.API_BASE_URL ||
  "http://127.0.0.1:8000";


// 배포용 config.js 생성
const configContent = `
window.APP_CONFIG = {
  API_BASE_URL: ${JSON.stringify(apiBaseUrl)}
};
`;

fs.writeFileSync(
  path.join(distDir, "config.js"),
  configContent
);

console.log(
  "Frontend build completed."
);

console.log(
  "API_BASE_URL:",
  apiBaseUrl
);