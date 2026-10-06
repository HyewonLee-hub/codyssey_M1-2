const API_BASE_URL =
  window.APP_CONFIG?.API_BASE_URL ||
  "http://127.0.0.1:8000";


// ==============================
// 데이터 요약
// ==============================

const summaryElement = document.querySelector("#summary");


async function loadSummary() {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/data/summary`
    );

    if (!response.ok) {
      throw new Error(
        "데이터 요약을 불러오지 못했습니다."
      );
    }

    const summary = await response.json();

    summaryElement.innerHTML = `
      <p>
        기간:
        ${summary.period.start}
        ~
        ${summary.period.end}
      </p>

      <p>
        데이터 개수:
        ${summary.count}개
      </p>

      <p>
        평균 PM10:
        ${summary.metrics.average} ㎍/㎥
      </p>

      <p>
        최대 PM10:
        ${summary.metrics.max} ㎍/㎥
      </p>

      <p>
        최소 PM10:
        ${summary.metrics.min} ㎍/㎥
      </p>

      <p>
        최근 추세:
        ${summary.trend}
      </p>
    `;

  } catch (error) {
    console.error(error);

    summaryElement.textContent =
      "데이터 요약을 불러올 수 없습니다.";
  }
}


// ==============================
// AI 채팅
// ==============================

const chatForm = document.querySelector("#chat-form");
const chatInput = document.querySelector("#chat-input");
const chatMessages = document.querySelector("#chat-messages");
const chatLoading = document.querySelector("#chat-loading");

let currentConversationId = null;


function addMessage(role, content) {
  const messageElement = document.createElement("div");

  messageElement.classList.add("message");

  if (role === "user") {
    messageElement.classList.add("user-message");
  } else {
    messageElement.classList.add("assistant-message");
  }

  messageElement.textContent = content;

  chatMessages.appendChild(messageElement);

  chatMessages.scrollTop = chatMessages.scrollHeight;
}


chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = chatInput.value.trim();

  if (!message) {
    return;
  }

  addMessage("user", message);

  chatInput.value = "";

  chatLoading.hidden = false;

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/chat`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          message: message,
          conversation_id: currentConversationId,
        }),
      }
    );

    if (!response.ok) {
      throw new Error(
        "AI 답변을 불러오지 못했습니다."
      );
    }

    const data = await response.json();

    currentConversationId = data.conversation_id;

    addMessage(
      "assistant",
      data.answer
    );

    await loadConversations();

  } catch (error) {
    console.error(error);

    addMessage(
      "assistant",
      "답변을 불러오는 중 오류가 발생했습니다."
    );

  } finally {
    chatLoading.hidden = true;
  }
});

const conversationList =
  document.querySelector("#conversation-list");

const newChatButton =
  document.querySelector("#new-chat-button");

async function loadConversations() {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/conversations`
    );

    if (!response.ok) {
      throw new Error(
        "대화 목록을 불러오지 못했습니다."
      );
    }

    const conversations = await response.json();

    conversationList.innerHTML = "";

    if (conversations.length === 0) {
      conversationList.textContent =
        "저장된 대화가 없습니다.";

      return;
    }

    conversations.forEach((conversation) => {
      const item = document.createElement("div");

      item.classList.add("conversation-item");

      const title = document.createElement("span");

      title.textContent =
        conversation.title || "제목 없는 대화";

      const deleteButton =
        document.createElement("button");

      deleteButton.textContent = "삭제";

      // 대화 클릭 → 해당 대화 불러오기
      item.addEventListener("click", () => {
        loadConversation(conversation.id);
      });

      // 삭제 버튼
      deleteButton.addEventListener(
        "click",
        async (event) => {
          event.stopPropagation();

          await deleteConversation(
            conversation.id
          );
        }
      );

      item.appendChild(title);
      item.appendChild(deleteButton);

      conversationList.appendChild(item);
    });

  } catch (error) {
    console.error(error);

    conversationList.textContent =
      "대화 기록을 불러올 수 없습니다.";
  }
}

async function loadConversation(conversationId) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/conversations/${conversationId}`
    );

    if (!response.ok) {
      throw new Error(
        "대화를 불러오지 못했습니다."
      );
    }

    const conversation = await response.json();

    // 현재 대화를 선택한 대화로 변경
    currentConversationId = conversation.id;

    // 기존 화면 메시지 제거
    chatMessages.innerHTML = "";

    // 저장된 메시지 다시 표시
    conversation.messages.forEach((message) => {
      addMessage(
        message.role,
        message.content
      );
    });

  } catch (error) {
    console.error(error);

    alert(
      "대화를 불러오는 중 오류가 발생했습니다."
    );
  }
}

async function deleteConversation(conversationId) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/conversations/${conversationId}`,
      {
        method: "DELETE",
      }
    );

    if (!response.ok) {
      throw new Error(
        "대화를 삭제하지 못했습니다."
      );
    }

    // 현재 보고 있던 대화를 삭제한 경우
    if (currentConversationId === conversationId) {
      currentConversationId = null;
      chatMessages.innerHTML = "";
    }

    await loadConversations();

  } catch (error) {
    console.error(error);

    alert(
      "대화를 삭제하는 중 오류가 발생했습니다."
    );
  }
}

newChatButton.addEventListener("click", () => {
  currentConversationId = null;

  chatMessages.innerHTML = "";

  chatInput.value = "";

  chatInput.focus();
});

const dataForm = document.querySelector("#data-form");
const dataDateInput = document.querySelector("#data-date");
const dataValueInput = document.querySelector("#data-value");
const dataMemoInput = document.querySelector("#data-memo");
const dataList = document.querySelector("#data-list");

async function loadData() {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/data`
    );

    if (!response.ok) {
      throw new Error(
        "데이터 목록을 불러오지 못했습니다."
      );
    }

    const data = await response.json();

    dataList.innerHTML = "";

    if (data.length === 0) {
      dataList.textContent =
        "저장된 데이터가 없습니다.";

      return;
    }

    // 데이터가 365개이므로 최근 20개만 화면에 표시
    const recentData = data.slice(-20).reverse();

    recentData.forEach((item) => {
      const row = document.createElement("div");

      row.classList.add("data-item");

      const info = document.createElement("span");

      info.textContent =
        `${item.date} | ${item.value} ㎍/㎥ | ${item.memo}`;

      const buttonArea = document.createElement("div");


      // 수정 버튼
      const editButton =
        document.createElement("button");

      editButton.textContent = "수정";

      editButton.addEventListener("click", () => {
        editData(item);
      });


      // 삭제 버튼
      const deleteButton =
        document.createElement("button");

      deleteButton.textContent = "삭제";

      deleteButton.addEventListener(
        "click",
        () => {
          deleteData(item.id);
        }
      );


      buttonArea.appendChild(editButton);
      buttonArea.appendChild(deleteButton);

      row.appendChild(info);
      row.appendChild(buttonArea);

      dataList.appendChild(row);
    });

  } catch (error) {
    console.error(error);

    dataList.textContent =
      "데이터를 불러오는 중 오류가 발생했습니다.";
  }
}

dataForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const date = dataDateInput.value;
  const value = Number(dataValueInput.value);
  const memo = dataMemoInput.value.trim();

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/data`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          date: date,
          value: value,
          memo: memo,
        }),
      }
    );

    if (response.status === 409) {
      alert(
        "해당 날짜의 데이터가 이미 존재합니다."
      );

      return;
    }

    if (!response.ok) {
      throw new Error(
        "데이터를 추가하지 못했습니다."
      );
    }

    // 입력칸 초기화
    dataForm.reset();

    // 목록 다시 조회
    await loadData();

    // Summary도 다시 계산해서 표시
    await loadSummary();

  } catch (error) {
    console.error(error);

    alert(
      "데이터 추가 중 오류가 발생했습니다."
    );
  }
});

async function deleteData(id) {
  const confirmed = confirm(
    `${id} 데이터를 삭제하시겠습니까?`
  );

  if (!confirmed) {
    return;
  }

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/data/${id}`,
      {
        method: "DELETE",
      }
    );

    if (!response.ok) {
      throw new Error(
        "데이터를 삭제하지 못했습니다."
      );
    }

    await loadData();
    await loadSummary();

  } catch (error) {
    console.error(error);

    alert(
      "데이터 삭제 중 오류가 발생했습니다."
    );
  }
}

async function editData(item) {
  const newValue = prompt(
    "새 PM10 값을 입력하세요.",
    item.value
  );

  if (newValue === null) {
    return;
  }

  const newMemo = prompt(
    "새 메모를 입력하세요.",
    item.memo
  );

  if (newMemo === null) {
    return;
  }

  const value = Number(newValue);

  if (Number.isNaN(value)) {
    alert("PM10 값은 숫자로 입력해주세요.");
    return;
  }

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/data/${item.id}`,
      {
        method: "PUT",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          value: value,
          memo: newMemo,
        }),
      }
    );

    if (!response.ok) {
      throw new Error(
        "데이터를 수정하지 못했습니다."
      );
    }

    await loadData();
    await loadSummary();

  } catch (error) {
    console.error(error);

    alert(
      "데이터 수정 중 오류가 발생했습니다."
    );
  }
}

loadSummary();
loadConversations();
loadData();