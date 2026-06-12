# 계좌 관리 어시스턴트 생성하기

## 실습 개요
이 실습에서는 **AI Assistant builder**를 사용하여 **계좌 개설 문의를 처리하는 계좌관리 어시스턴트**를 생성합니다.

사용자가 계좌 개설을 요청하면, 어시스턴트가 계좌 유형을 확인하고 다음과 같이 분기하여 응답하도록 구성합니다.

- **투자예금** 선택 시: 투자 번호를 입력받은 뒤 상담원에게 연결
- **당좌예금 / 저축예금** 선택 시: 계좌 개설 포털 링크로 안내

---

## 실습 목표
이 실습을 완료하면 다음을 수행할 수 있습니다.

- 새 AI Assistant를 생성할 수 있다.
- Action을 생성하고 Phrase를 학습시킬 수 있다.
- Step 기반 대화 흐름을 구성할 수 있다.
- 조건(Conditions)을 사용해 분기 로직을 만들 수 있다.
- 사용자 입력값을 변수로 활용할 수 있다.
- Preview를 통해 동작을 테스트할 수 있다.

---

## 최종 시나리오
최종적으로 아래와 같은 흐름의 계좌 개설 어시스턴트를 완성합니다.

1. 사용자가 계좌 개설 의도를 말한다.
2. 어시스턴트가 계좌 유형을 묻는다.
3. 사용자가 **투자예금**을 선택하면 투자 번호를 추가로 묻는다.
4. 투자 번호를 입력하면 상담원에게 연결한다.
5. 사용자가 **당좌예금** 또는 **저축예금**을 선택하면 계좌 개설 포털 링크를 안내한다.

---

## 사전 준비
실습을 시작하기 전에 다음 항목을 준비합니다.

- watsonx Orchestrate 접속 계정
- AI Assistant builder 접근 권한
- 포털 시스템 URL 예시  
  예:[www.ibm-bank.com/open-a-new-account?account_type=](http://www.ibm-bank.com/open-a-new-account?account_type=)
- 상담원 연결을 시연할 경우 사용할 연동 환경(선택)

---

# 1. AI Assistant 생성하기

## 1-1. watsonx Orchestrate 접속
watsonx Orchestrate에 로그인합니다.

## 1-2. AI Assistant builder 진입
왼쪽 메뉴에서 **AI Assistant builder**로 이동합니다.

## 1-3. 새 Assistant 생성
**Create assistant** 또는 **New Assistant** 버튼을 클릭하여 새 Assistant를 생성합니다.
![create_assistant](./ai_assistant_img/img1.png)

- **Assistant 이름 예시**
```

<사용자명>_Account_Management_Assistant

```

- **설명 예시**
```

신규 계좌 개설 문의를 처리하는 계좌관리 Assistant

```

Assistant 생성이 완료되면 다음 단계로 이동합니다.

---

# 2. Personalize 단계

Create 단계 다음에는 **Personalize** 단계가 나타납니다.  
이 단계에서는 Assistant의 소개 문구, 시작 메시지, 추천 프롬프트 등을 설정할 수 있습니다.

> **참고**  
> 이번 실습의 핵심은 **계좌 개설 Action 구성과 Step 분기 로직**입니다.  
> 따라서 **Personalize 단계는 자유롭게 작성하거나 기본값으로 두고 넘어가겠습니다.**

설정을 마친 뒤 다음 단계로 이동합니다.

---

# 3. Action 생성하기

## 3-1. 새 Action 생성하기
**Actions** 메뉴로 이동한 뒤 **Create action** 또는 **New Action**을 선택합니다.
![new_actions](./ai_assistant_img/img2.png)
![create_actions](./ai_assistant_img/img3.png)
이 실습에서는 사용자의 계좌 개설 요청을 처리하는 Action을 생성합니다.

## 3-2. Action명 작성하기
새 Action 생성 화면에서 액션 이름을 입력합니다.
![action_name](./ai_assistant_img/img4.png)
- **액션명 예시**
```

새 당좌 예금 계좌를 개설하고 싶습니다

```

---

# 4. Action 인식 문구(Phrases) 작성하기

## 4-1. 기본 인식 테스트
**Customer starts with** 영역에서 Action을 트리거할 문구를 학습시킵니다.

- **Preview** 버튼을 클릭합니다.  
![test_action1](./ai_assistant_img/img5.png)

- 채팅창에 아래 문구를 입력합니다.

```
계좌 개설

새로운 계좌를 개설하고 싶습니다.

계좌 개설 종류는 무엇이 있나요?

개설할 수 있는 계좌는 무엇이 있나요?

어떤 유형의 계좌 개설에 도움을 줄 수 있나요?
```
![alt text](./assistant_image/image032.png)

- 아직 충분히 학습되지 않은 경우, Action을 바로 인식하지 못할 수 있습니다.  
이 경우 **Debug** 기능을 통해 문구 이해도를 확인합니다.  
![alt text](./assistant_image/image033.png)

- 예를 들어 `계좌 개설`에 대한 이해도가 낮게 표시될 수 있습니다.  
![alt text](./assistant_image/image035.png)

## 4-2. Phrase 추가 학습
- **Add example phrases** 입력란에 아래 문구를 추가하고 Enter를 누릅니다.
![add phrases](./ai_assistant_img/img7.png)
```

계좌 개설

```


- 새로운 문구가 Action을 트리거할 수 있도록 학습이 진행됩니다.  
![alt text](./assistant_image/image037.png)

- 학습이 완료되면 다시 Preview에서 아래 문구를 입력합니다.
```

계좌 개설

````

- 이제 Action이 정상적으로 인식되고 트리거되는 것을 확인할 수 있습니다.  
![alt text](./assistant_image/image038.png)

- 이해도가 높아진 것도 확인할 수 있습니다.  
![alt text](./assistant_image/image039.png)

## 4-3. 참고
- 각 문구의 길이는 최대 1,024자입니다.
- 사용자가 실제로 입력할 수 있는 다양한 표현을 계속 추가해 주면 Assistant의 인식률을 높일 수 있습니다.

---

# 5. Step 생성하기

## 5-1. 첫 번째 Step 작성하기
**New Step** 버튼을 클릭하여 첫 번째 Step을 추가합니다.

이제 계좌 개설 상호작용의 첫 단계를 구성합니다.  
먼저 고객이 원하는 계좌 유형을 묻는 질문을 만듭니다.

### Assistant says
아래 문구를 입력합니다.
```text
어떤 유형의 계좌를 개설하시겠습니까?
````
![assistant_says](./ai_assistant_img/img8.png)

### Define customer response

**Define customer response > Options** 를 선택합니다.

팝업창에서 아래 3개의 옵션을 추가합니다.

* 당좌예금
* 저축예금
* 투자예금

![alt text](./assistant_image/image001.png)

### Preview 테스트

**Preview** 버튼을 클릭하여 아래 문구로 동작을 확인합니다.

```text
새 계좌를 개설할 수 있나요?
```

![alt text](./assistant_image/image002.png)

첫 번째 Step이 완료되었습니다.

---

## 5-2. 두 번째 Step 작성하기

**New Step** 버튼을 클릭하여 두 번째 Step을 추가합니다.

이 Step은 사용자가 첫 번째 Step에서 **투자예금**을 선택한 경우에만 실행되도록 만듭니다.
투자예금의 경우 고객으로부터 **투자 번호**를 입력받아야 합니다.

### with conditions 설정

* **with conditions** 을 선택합니다.
![with columns](./ai_assistant_img/img9.png)

* 첫 번째 Step인
  `어떤 유형의 계좌를 개설하시겠습니까?`
  에서 사용자가 **투자예금**을 선택한 조건을 설정합니다.

* 조건 작성 시 **Action step variables** 를 선택합니다.<br>
  ![alt text](./ai_assistant_img/img.png)

* `1. 어떤 유형의 계좌를 개설하시겠습니까?` 를 선택합니다.
  ![alt text](./ai_assistant_img/img10.png)

* 조건 값으로 **투자예금**을 선택합니다.
  ![alt text](./ai_assistant_img/img11.png)

* 설정이 완료되면 아래와 같이 조건이 구성됩니다.
  ![alt text](./assistant_image/image003.png)

### Assistant says

아래 문구를 입력합니다.

```text
당신의 투자 번호가 무엇입니까?
```

![alt text](./ai_assistant_img/img12.png)

### Define customer response

**Define customer response > Number** 를 선택합니다.
![alt text](./ai_assistant_img/img13.png)<br>

사용자로부터 투자 번호를 입력받도록 설정합니다.
![alt text](./assistant_image/image008.png)<br>

### Preview 테스트

**Preview** 버튼을 클릭하여 동작을 확인합니다.<br>
![alt text](./assistant_image/image009.png)

두 번째 Step이 완료되었습니다.

---

## 5-3. 세 번째 Step 작성하기

**New Step** 버튼을 클릭하여 세 번째 Step을 추가합니다.
![alt text](./ai_assistant_img/img14.png)

이제 사용자가 **투자예금**을 선택했고, **투자 번호**까지 입력한 경우 상담원에게 연결하는 과정을 만듭니다.

### with conditions 설정

* **with conditions** 을 선택합니다.
![with conditions](./ai_assistant_img/img15.png)

* 첫 번째 조건으로
  `1. 어떤 유형의 계좌를 개설하시겠습니까?` = `투자예금`
  을 설정합니다.

* 이어서 **Add condition +** 버튼을 클릭하여 두 번째 조건을 추가합니다.
  ![alt text](./ai_assistant_img/img16.png)<br>

* 필요한 조건 구성을 완료합니다.<br>
  ![alt text](./assistant_image/image010.png)

### Assistant says

아래 문구를 입력합니다.

```text
귀하를 위해 새로운 투자 계좌를 개설할 수 있는 에이전트에게 연결해 드리겠습니다!
```

![alt text](./ai_assistant_img/img17.png)

### And then 설정

**And then > Continue to next step > Connect to agent** 를 선택합니다.
![alt text](./ai_assistant_img/img18.png)


### Message to agent 설정

상담원에게 전달할 메시지를 작성합니다.
![message to agent](./ai_assistant_img/img19.png) <br>
예시:

```text
고객이 원하는 투자 번호는
```

![alt text](./assistant_image/image040.png)<br>

이어서 사용자 입력값을 변수로 전달하기 위해 `$` 를 입력하여 변수를 선택합니다.<br>
![alt text](./assistant_image/image041.png)

다음 경로를 선택합니다.

```text
Action step variables > 2. 당신의 투자 번호가 무엇입니까?
```

![alt text](./assistant_image/image042.png)

마지막으로 문장을 완성합니다.

```text
입니다
```

![alt text](./assistant_image/image043.png)<br>

최종적으로 상담원에게 전달되는 메시지는 다음과 같은 형태가 됩니다.

```text
고객이 원하는 투자 번호는 [사용자 입력값]입니다
```

Agent 연결 설정이 완료되면 아래와 같이 구성됩니다.<br>
![alt text](./assistant_image/image044.png)<br>

### Preview 테스트

**Preview** 버튼을 클릭하여 동작을 확인합니다.<br>
![alt text](./assistant_image/image015.png)<br>

세 번째 Step이 완료되었습니다.

---

## 5-4. 네 번째 Step 작성하기

**New Step** 버튼을 클릭하여 네 번째 Step을 추가합니다.

이 Step은 사용자가 **당좌예금** 또는 **저축예금**을 선택한 경우, 계좌 개설 포털로 안내하는 과정입니다.

### with conditions 설정

* **with conditions** 을 선택합니다.
![with columns](./ai_assistant_img/img21.png)<br>
* 첫 번째 Step인
  `어떤 유형의 계좌를 개설하시겠습니까?`
  의 결과를 조건으로 사용합니다.

* **Action step variables** 를 선택합니다.<br>
  ![alt text](./assistant_image/image004.png)<br>

* `1. 어떤 유형의 계좌를 개설하시겠습니까?` 를 선택합니다.<br>
  ![alt text](./assistant_image/image005.png)<br>

* 조건 유형으로 **is any of** 를 선택합니다.<br>
  ![alt text](./assistant_image/image016.png)<br>

* 조건 값으로 아래 두 개를 선택합니다.<br>

  * 당좌예금
  * 저축예금

  ![alt text](./assistant_image/image017.png)<br>

* 설정 완료 화면은 아래와 같습니다.<br>
  ![alt text](./assistant_image/image018.png)<br>

### Assistant says

이 Step에서는 사용자가 선택한 계좌 유형을 메시지에 포함하여 안내합니다.

* 메시지 작성 화면에서 **fx** 버튼을 클릭합니다.
![function](./ai_assistant_img/img24.png)
* 팝업창에서 **Action step variables** 를 선택합니다.
  ![alt text](./assistant_image/image019.png)

* 첫 번째 Step
  `어떤 유형의 계좌를 개설하시겠습니까?`
  를 선택합니다.
  ![alt text](./assistant_image/image020.png)<br>
  ![alt text](./assistant_image/image021.png)<br>

* 이어서 아래 텍스트를 입력합니다.

  ```text
  계좌 개설을 위해
  ```

  ![alt text](./assistant_image/image022.png)<br>

### 링크 삽입

포털 주소 링크를 삽입합니다.

* 링크 아이콘을 클릭합니다.
  ![alt text](./assistant_image/image023.png)<br>

* 포털 시스템의 계좌 개설 주소를 입력합니다. 예:

  ```text
  www.ibm-bank.com/open-a-new-account?account_type=
  ```

  ![alt text](./assistant_image/image024.png)<br>

* URL 뒤에 변수 값을 전달하기 위해 `$` 를 입력하여 변수 선택 창을 엽니다.
  ![alt text](./assistant_image/image025.png)<br>

* 아래 변수를 선택합니다.

  ```text
  Action step variables > 1. 어떤 유형의 계좌를 개설하시겠습니까?
  ```

  ![alt text](./assistant_image/image026.png)<br>

* **Apply** 를 클릭하여 설정을 적용합니다.<br>
  ![alt text](./assistant_image/image027.png)<br>

* 마지막으로 아래 안내 문구를 입력합니다.

  ```text
  에 방문해 주세요.
  ```

  ![alt text](./assistant_image/image028.png)<br>

### And then 설정

**And then > End the action** 을 선택합니다.<br>
![alt text](./ai_assistant_img/img27.png)<br>

이 Step의 최종 종료 설정이 완료되었습니다.<br>
![alt text](./assistant_image/image030.png)<br>

### Preview 테스트

**Preview** 버튼을 클릭하여 동작을 확인합니다.<br>
![alt text](./assistant_image/image015.png)<br>

네 번째 Step이 완료되었습니다.

---

# 6. 테스트 시나리오

## 시나리오 1. 투자예금 선택

입력 예시:

```text
계좌 개설
```

예상 흐름:

1. 어떤 유형의 계좌를 개설하시겠습니까?
2. 투자예금 선택
3. 투자 번호 입력
4. 상담원 연결

## 시나리오 2. 당좌예금 선택

입력 예시:

```text
새 계좌를 만들고 싶어요
```

예상 흐름:

1. 어떤 유형의 계좌를 개설하시겠습니까?
2. 당좌예금 선택
3. 계좌 개설 포털 링크 안내
4. Action 종료

## 시나리오 3. 저축예금 선택

입력 예시:

```text
저축 계좌 개설하고 싶어요
```

예상 흐름:

1. 어떤 유형의 계좌를 개설하시겠습니까?
2. 저축예금 선택
3. 계좌 개설 포털 링크 안내
4. Action 종료

---

# 7. 완료된 화면

최종 완료된 화면입니다.
총 4개의 Step으로 구성되며, 인식이 부족한 문구는 Phrase를 추가하여 계속 학습시킬 수 있습니다.<br>
![alt text](./assistant_image/image048.png)<br>

---

# 8. AI Assistant 배포하기

이렇게 AI Assistant의 기본 구조가 완성되었습니다.

이제 완성된 AI Assistant를 배포해 Agent에게 전달해보겠습니다.

![publish menu](./call_assistant/publish.png)

**햄버거 메뉴를 눌러 Assistant builder 메뉴로 돌아갑니다.**

![publish menu2](./call_assistant/publish2.png)

**Assistant의 List 화면에서 Publish 메뉴를 클릭합니다.**

![publish menu3](./call_assistant/publish3.png)
**Publish 버튼을 눌러 Publish version create 창을 엽니다.**

![publish menu4](./call_assistant/publish4.png)<br>
**새로운 버전에 대한 변경사항을 기입하고, Publish an environment 드롭다운에서 Live를 선택한 뒤, Publish 버튼을 클릭합니다.**

**이제 Create Agent 단계에서 지금 생성된 AI Assistant를 사용할 수 있게 되었습니다.**<br>

**다음으로는 Agent를 생성하여 AI Assistant를 호출해보겠습니다.**

