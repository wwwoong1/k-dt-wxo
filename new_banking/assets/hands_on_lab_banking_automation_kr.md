# 인텔리전트 에이전트를 활용한 뱅킹 혁신 - 실습 <!-- omit in toc -->

## 사전 준비사항 
- AI Assistant 구축 (Account Management Assistant)
- **[Create Assistant 바로가기](https://github.com/wwwoong1/k-dt-wxo/blob/main/new_banking/AI_Assistant/README.md)**

## 목차 <!-- omit in toc -->

- [🔍 소개](#-소개)
- [📊 뱅킹 운영](#-뱅킹-운영)
  - [현재 사용자 시나리오](#현재-사용자-시나리오)
  - [에이전트 AI와 함께하는 미래](#에이전트-ai와-함께하는-미래)
- [🏗️ 에이전트 AI 기반 목표 아키텍처](#️-에이전트-ai-기반-목표-아키텍처)
- [🔧 실습 안내](#-실습-안내)
  - [사전 준비 사항](#사전-준비-사항)
  - [실습 단계 개요](#실습-단계-개요)
- [할당받은 Watsonx Orchestrate 인스턴스에 연결](#할당받은-watsonx-orchestrate-인스턴스에-연결)
- [GFM 백오피스 에이전트(예:Seongman_BackOfficeAgent)](#gfm-백오피스-에이전트예Seongman_backofficeagent)
  - [GFM 백오피스 에이전트 생성](#gfm-백오피스-에이전트-생성)
  - [GFM 백오피스 에이전트 테스트 및 배포](#gfm-백오피스-에이전트-테스트-및-배포)
- [GFM 텔러 에이전트(예:Seongman_TellerAgent)](#gfm-텔러-에이전트예Seongman_telleragent)
  - [GFM 텔러 에이전트 생성](#gfm-teller-agent-생성하기)
  - [GFM 텔러 에이전트 테스트 및 배포](#gfm-teller-agent-테스트-및-배포)
- [GFM 상품 정보 에이전트(예:Seongman_ProductInformationAgent)](#gfm-상품-정보-agent-예Seongman_productinformationagent)
  - [GFM 상품 정보 에이전트 생성](#gfm-상품-정보-에이전트-생성)
  - [GFM 상품 정보 에이전트 테스트 및 배포](#gfm-product-information-agent-테스트-및-배포)
- [GFM 은행 오케스트레이터 에이전트(예:Seongman_AskGFMBank)](#gfm-bank-orchestrator-agent-예Seongman_askgfmbank)
  - [GFM 은행 오케스트레이터 에이전트 생성](#gfm-bank-orchestrator-agent-생성)
  - [협업 에이전트 추가](#협업-에이전트-추가)
  - [GFM 은행 오케스트레이터 에이전트 테스트 및 배포](#gfm-bank-orchestrator-agent-테스트-및-배포)
- [에이전트 AI 뱅킹 솔루션 테스트](#gfm-bank-orchestrator-agent-테스트-및-배포)
- [🎉 실습 완료!](#-실습-완료)
- [📚 참고 자료](#-참고-자료)

## 🔍 소개

GFM Bank 에이전트 AI 실습에 오신 것을 환영합니다! 이 실습에서는 기존 뱅킹 애플리케이션을 **watsonx Orchestrate**를 활용하여 AI 기반 솔루션으로 전환합니다. 금융 산업은 빠른 디지털 전환을 겪고 있으며, GFM Bank는 고객 상호작용을 처리하기 위해 혁신적인 AI 에이전트를 구현하여 선도하고 있습니다.

기존 GFM Bank는 인간 텔러와 백오피스 직원에 의존하여 수작업으로 운영되어, 고객 대기 시간이 길고 운영 효율이 낮았습니다. 에이전트 AI 솔루션을 구현함으로써 은행은 다음을 목표로 합니다:

- 일반적인 뱅킹 업무에 대해 24/7 고객 지원 제공  
- 거래 및 승인 처리 대기 시간 단축  
- 금융 규제 준수 유지  
- 신속한 서비스 제공을 통한 고객 만족도 향상  
- 직원이 보다 복잡한 고객 요청을 처리할 수 있도록 지원  

이번 실습에서는 협업하는 AI 에이전트 시스템을 구축하여 다음과 같은 뱅킹 업무를 처리할 수 있습니다:

- 계좌 잔액 조회  
- 계좌 간 송금  
- 당좌 대월 승인  
- 수수료 환불  
- 상품 정보 요청  

## 📊 뱅킹 운영

*현재 GFM Bank는 기본 거래를 위해 인간 텔러를, 승인 처리를 위해 백오피스 직원을 활용하며, 성수기에는 지연과 일관성 없는 고객 경험이 발생합니다.*

### 현재 사용자 시나리오

고객 John은 긴급하게 €8,000를 송금해야 하지만 계좌에 €5,000만 보유하고 있습니다.

1. John은 은행 지점을 방문하여 텔러를 기다립니다  
2. 텔러가 계좌 잔액을 확인하고 부족하다고 안내합니다  
3. John은 €3,000 당좌 대월을 요청합니다  
4. 텔러는 백오피스 관리자에게 요청을 전달합니다  
5. John은 승인을 기다립니다  
6. 승인 후 다시 텔러에게 돌아와 송금을 완료합니다  
7. 만약 송금 금액을 잘못 보냈다면, 환불 요청을 위해 다시 승인 절차를 거쳐야 합니다  

이 과정은 일반적으로 1~2시간이 소요되며, 여러 직원이 참여합니다.

### 에이전트 AI와 함께하는 미래

AI 기반 시스템에서는:

1. John이 GFM 은행 오케스트레이터 에이전트에 메시지 전송  
2. €8,000 송금을 요청  
3. 텔러 에이전트가 잔액 확인 및 부족 안내  
4. John이 당좌 대월 요청  
5. 텔러 에이전트가 요청을 백오피스 에이전트로 전달  
6. 백오피스 에이전트가 €10,000 미만 요청 승인 시, 텔러 에이전트가 송금 완료  
7. 환불 요청이 필요하면, 동일한 대화 내에서 신속하게 처리  

전체 과정이 몇 분 내로 완료되며, John은 집을 떠날 필요가 없습니다.

## 🏗️ 에이전트 AI 기반 목표 아키텍처

![Architecture](banking-backoffice-architecture.png)

## 🔧 실습 안내

이번 실습에서는 watsonx Orchestrate를 활용하여 GFM Bank용 완전한 에이전트 AI 솔루션을 구축합니다. 고객 요청을 처리하기 위해 서로 협업하는 전문 에이전트를 여러 개 생성합니다.

### 사전 준비 사항

- 강사에게 시스템 정상 작동 여부 확인  
- 실습 환경용 TechZone 접근 권한 확인  
- 강사가 제공한 자격 증명 파일 확인  
- 강사용: 모든 환경 및 시스템 세팅 가이드 확인  
- 기본적인 뱅킹 업무 이해 (송금, 잔액 조회, 당좌 대월 등)  
- AI 에이전트 개념 이해 (지침, 도구, 협업자 등)  

### 실습 단계 개요

1. **watsonx Orchestrate**에 연결  
2. GFM 백오피스 에이전트 생성  
3. GFM 텔러 에이전트 생성  
4. GFM 상품 정보 에이전트 생성  
5. GFM 은행 오케스트레이터 에이전트 생성  
6. 전체 솔루션 테스트




### 🚀🚀🚀 시작해봅시다! 🚀🚀🚀 <!-- omit in toc -->

### 할당받은 Watsonx Orchestrate 인스턴스에 연결

- IBM Cloud (cloud.ibm.com)에 로그인합니다. 좌측 상단 햄버거 메뉴에서 **리소스 목록(Resource List)**으로 이동합니다. AI/머신러닝 섹션에서 **watsonx Orchestrate** 서비스를 확인하고 클릭하여 엽니다.

  ![Watsonx Orchestrate 서비스](./images/i1.png)

- **watsonx Orchestrate 시작(Launch watsonx Orchestrate)** 버튼을 클릭합니다.

  ![Watsonx Orchestrate 시작](./images/i2.png)

- watsonx Orchestrate에 오신 것을 환영합니다. 햄버거 메뉴를 열고 **Build** -> **Agent Builder**를 클릭합니다.

  ![Agent Builder](./images/i3.png)

### GFM 백오피스 에이전트(예:Seongman_BackOfficeAgent)

이 에이전트는 GFM Bank의 특수 은행 업무를 처리하며, 당좌 대월 승인이나 수수료 환불 처리와 같이 높은 권한이 필요한 작업을 수행합니다. GFM Bank 운영 센터에서 운영됩니다.


#### GFM 백오피스 에이전트 생성

- **Create Agent** 버튼을 클릭합니다.

  ![Create Agent](./backoffice_ag_imgs/i1.png)

- 아래 스크린샷과 같이 단계를 진행합니다.
  - **Create from scratch** 선택   
  - 에이전트 이름 입력:
    **주의사항** : 명명규칙
    - 다수의 인원이 한 자원을 사용하므로 반드시 명명규칙을 지켜 주시기 바랍니다.
    - 명명규칙 : <자기이름>_BackOfficeAgent
    - 이름 (예) : 
      ```
      Seongman_BackOfficeAgent
      ```
  - **설명(Description)** 
    ```
    당신은 GFM Bank의 백오피스 에이전트로, 높은 권한이 필요한 특별 은행 업무를 처리합니다. GFM Bank 운영 센터에서 근무하며 당좌 대월 승인과 수수료 환불 처리를 담당합니다.

    당신의 역량:
    1. `approve-overdraft` 도구를 사용하여 IBAN과 금액(0~10,000 EUR)으로 당좌 대월 한도 승인
    2. `fee-reversal` 도구를 사용하여 IBAN과 금액으로 수수료 환불 처리
    3. 특별 예외 또는 조정 사항 처리
    4. 높은 권한이 필요한 모든 작업 수행
    5. 요청 시 환불 제공
    ```
  - **Create** 클릭

    ![Back Office Agent Description](./backoffice_ag_imgs/i2.png)

- GFM 백오피스 페이지에서 상단 중앙 드롭다운 메뉴에서 "llama-3-405b-instruct" 모델 선택

  ![Select Model](./backoffice_ag_imgs/i15.png)

- **Profile**, **Voice modality**, **Knowledge** 섹션은 기본값 유지
- **Toolset** 섹션에서 **Add tool** 버튼 클릭

  ![Add Tool](./backoffice_ag_imgs/i3.png)

- **Open API** 클릭

  ![Import file](./backoffice_ag_imgs/i4.png)


- 강사가 제공한 `bank.yaml` API 스펙 파일 업로드

  ![Upload spec file](./images/i38.png)

- 파일 업로드 후 **Next** 클릭, "Process a fee reversal to an account"와 "Approve or modify overdraft limit for an account" **Operations** 선택 후 **Done** 클릭

  ![Select Tools](./backoffice_ag_imgs/i7.png)

- **Tools** 섹션에서 다음과 같이 표시됩니다.

  ![Loaded tools](./backoffice_ag_imgs/i9.png)

- **Behavior** 섹션에서 **Instructions**에 다음 내용 추가:
  ```
    핵심 지침:
    - 고객이 명시적으로 요청한 작업만 실행하세요.
    - 어떤 작업을 수행하기 전에 세부 정보를 검증하세요.
    - 완료된 모든 작업에 대해 반드시 확인 응답을 제공하세요.
    - 오류나 제한 사항이 있으면 명확하게 설명하세요.
    
    규칙 및 제한 사항:
    - 당좌대월 한도는 1,000 EUR에서 10,000 EUR 사이여야 합니다.
    - 고객이 명확한 업무상 사유를 제공한 경우에만 수수료 환불을 처리하세요.
    - 어떤 작업을 처리하든 항상 IBAN을 먼저 확인하세요.
    - 전문적이고 효율적인 태도를 유지하세요.
    
    응답 가이드라인:
    - 당좌대월 승인 요청의 경우: 승인 또는 거절 여부를 알리고, 새로운 한도와 계좌 정보를 보여주세요.
    
    응답 예시:
    2,000 EUR 금액에 대한 당좌대월이 승인되었습니다.
    
    - 수수료 환불의 경우: 환불된 금액과 새로운 계좌 잔액을 확인해 주세요.
    - 오류의 경우: 문제를 명확히 설명하고, 적절하다면 대체 가능한 해결책을 제안하세요.
    - 항상 수행한 작업이 무엇인지 명확히 드러나는 간결한 언어를 사용하세요.
    
    높은 권한을 가진 은행 담당자에 적합한 수준의 격식과 전문성을 갖춘 어조를 유지하세요.
  ```




#### GFM 백오피스 에이전트 테스트 및 배포

- 오른쪽 미리보기 창에서, 할당받은 IBAN을 사용하여 다음 쿼리로 테스트:

  ```
  내 계좌 IBAN DE89320895326389021994에 대해 1000유로 당좌대월을 요청하고 싶습니다.
  ```
- Channels > Home page 를 disable 처리 함
- **Deploy** 버튼을 클릭하여 에이전트 배포

![Deploy](./backoffice_ag_imgs/i10.png)

- **Deploy Agent** 페이지에서 **Deploy** 클릭

![Deploy agent](./backoffice_ag_imgs/i13.png)





### GFM 텔러 에이전트(예:Seongman_TellerAgent)

이 에이전트는 고객의 일상적인 은행 업무(잔액 조회, 송금 등)를 지원합니다. 요청된 사항에 대해서만 응답하며, 가정이나 사전 행동은 수행하지 않습니다.

#### GFM Teller Agent 생성하기

- 햄버거 메뉴를 클릭한 뒤 **Build** -> **Agent Builder** 선택

  ![Agent Builder](./images/i3.png)

- **Create Agent** 클릭

  ![Create Agent](./teller_ag_imgs/i2.png)

- 아래 스크린샷에 따라 단계를 진행합니다.  
  - **Create from scratch** 선택  
  - 에이전트 이름 입력
    **주의사항** : 명명규칙
    - 다수의 인원이 한 자원을 사용하므로 반드시 명명규칙을 지켜 주시기 바랍니다.
    - 명명규칙 : <자기이름>_TellerAgent
    - 이름 (예) : 
      ```
      Seongman_TellerAgent
      ```
  - **설명(Description)** 
    ```
    당신은 GFM Bank의 TellerAgent로, 잔액 조회와 이체 같은 은행 거래 업무를 정확하고 전문적으로 지원하는 역할을 맡고 있습니다. 고객이 요청한 내용에만 엄격하게 응답하며, 추측하거나 제안하지 않습니다.
    
    당신이 할 수 있는 일:
    - IBAN을 사용하여 balance-inquiry 도구로 계좌 잔액 확인
    - 출금 계좌 IBAN, 입금 계좌 IBAN, 금액을 사용하여 iban-transfer 도구로 송금 처리
    - 잔액 응답 시 최근 거래 내역을 보기 좋은 목록 또는 표 형식으로 구조화하여 제공
    
    다음과 같은 경우 Back Office Agent로 라우팅:
    - 고객이 당좌대월 승인 또는 한도 변경을 요청하는 경우
    - 고객이 수수료 취소 또는 환불을 요청하는 경우
    - 고객에게 특별 예외나 조정이 필요한 경우
    - 높은 권한이 필요한 작업이 의도에 포함된 경우
    - 고객이 다음과 같은 표현을 사용하는 경우: "당좌대월이 필요해요", "수수료를 취소해 주세요", "환불을 요청합니다"
    ```

- **Create** 클릭
 
  ![Create agent](./teller_ag_imgs/i5.png)

- `자신이 만든 Teller 에이전트 (예:Seongman_TellerAgent)` 페이지에서, 화면 상단 중앙의 드롭다운 메뉴에서 "llama-3-405b-instruct" 모델을 선택합니다.

  ![Select model](./teller_ag_imgs/i20.png)

- **Profile**, **Voice modality**, **Knowledge** 항목은 기본값을 그대로 둡니다.  
  **Toolset** 섹션에서 **Add tool** 버튼을 클릭합니다.

  ![Add Tool](./teller_ag_imgs/i6.png)

- **OpenAPI** 클릭

  ![Import](./teller_ag_imgs/i7.png)



- 강사로부터 제공받은 `bank.yaml` API 사양 파일을 업로드합니다.  
  파일 업로드가 완료되면 **Next** 선택.
  
  ![Upload spec file](./images/i38.png)

- "Check account balance by IBAN" 과 "Transfer Money between IBANs" **Operations** 를 선택 후 **Done** 클릭.

  ![Select Operations](./teller_ag_imgs/i10.png)

- **Tools** 항목에 아래와 같이 표시됩니다.
  
  ![Uploaded tools](./teller_ag_imgs/i12.png)

- **Agents** 섹션에서 **Add Agent** 클릭

  ![Uploaded tools](./teller_ag_imgs/i16.png)

- **Local instance** 클릭

  ![Uploaded tools](./teller_ag_imgs/i17.png)

- **자신이 만든 에이전트(예:Seongman_BackOfficeAgent)** 선택 후 **Add to Agent** 버튼 클릭

  ![Uploaded tools](./teller_ag_imgs/i18.png)

  ![Uploaded tools](./teller_ag_imgs/i19.png)

- **Behavior** 섹션으로 이동하여, **Instructions**에 다음 내용을 추가:
  ```
  고객이 명확하게 요청한 내용에만 응답하세요. 다음 단계는 절대 미리 추측하거나 제안하지 마세요.
  의도를 추정하지 마세요. 문의나 요청이 불분명하면 반드시 추가 확인 질문을 하세요.
  전문적인 어조로 명확하고 간결하게 말하세요.
  
  송금 요청의 경우 다음을 수행하세요:
  - 송금을 확인하고 처리하세요.
  - 성공 또는 실패 여부를 알려주세요. 성공한 경우 처리 결과를 함께 알려주세요.
  - 잔액 부족 시에는 실패 사실만 알리고, 고객이 명시적으로 요청하지 않는 한 당좌대월을 제안하지 마세요.
  
  잔액 조회의 경우:
  - 현재 잔액을 표시하세요.
  - 사용 가능한 경우 당좌대월 한도를 표시하세요.
  - 최근 거래 내역을 표 또는 글머리표 목록 형식으로 표시하세요.
  - 응답은 거기서 끝내세요. 추가 행동을 제안하지 마세요.
  
  잔액 조회 시 최근 거래 내역은 다음 형식으로 제시하세요:
  고객: "IBAN DE12345678 계좌 잔액이 얼마인가요?"
  에이전트:
  현재 잔액은 500 EUR입니다.
  당좌대월 한도는 200 EUR입니다.
  
  최근 거래 내역:
  | 날짜 | 유형 | 금액 | 설명 |
  |------|------|------|------|
  | 5월 16일 | 출금 | -50 EUR | ATM 출금 |
  | 5월 15일 | 입금 | +200 EUR | 급여 입금 |
  | 5월 13일 | 결제 | -30 EUR | 식료품점 |
  ```

- 이 에이전트는 **GFM Bank Orchestrator Agent**에 의해 호출되는 협업 에이전트이므로, 채팅 홈 화면에서 직접 사용하도록 활성화하지 않습니다.  
**Home page** 기능을 비활성화합니다.

![Home page toggle](./teller_ag_imgs/i14.png)










#### GFM Teller Agent 테스트 및 배포

- 오른쪽 미리보기 창에서 다음 질의로 테스트합니다:

```
내 계좌 IBAN DE89320895326389021994의 잔액이 얼마인가요?
```

- **Deploy** 를 클릭하여 에이전트를 배포합니다.

  ![Deploy](./teller_ag_imgs/i13.png)

- **Deploy Agent** 화면에서 **Deploy** 클릭.  
  이제 이 에이전트는 다른 사용자가 상호작용할 수 있도록 사용 가능합니다.

  ![Deploy agent](./teller_ag_imgs/i1.png)
  







### GFM 상품 정보 Agent (예:Seongman_ProductInformationAgent)

이 에이전트는 GFM 은행에서 제공하는 모든 금융 상품과 서비스에 대한 신뢰할 수 있는 전문가 역할을 합니다.  
고객이 제공되는 금융 솔루션을 명확하고 정확하게 탐색하고 이해할 수 있도록 도와줍니다.



#### GFM 상품 정보 에이전트 생성

- 햄버거 메뉴 클릭 후, **Build** 선택

  ![Agent Builder](./images/i3.png)

- 다음 화면에서 **Create Agent** 클릭

  ![Create Agent](./prod_info_ag_imgs/i1.png)

- 아래 스크린샷에 따라 단계 진행
  - **Create from scratch** 선택
  - 에이전트 이름 입력
    **주의사항** : 명명규칙
    - 다수의 인원이 한 자원을 사용하므로 반드시 명명규칙을 지켜 주시기 바랍니다.
    - 명명규칙 : <자기이름>_ProductInformationAgent
    - 이름 (예) : 
      ```
      Seongman_ProductInformationAgent
      ```
  - **설명(Description)** 
    ```
    당신은 GFM 은행의 모든 상품과 서비스에 대한 전문 리소스입니다.  
    정확하고 명확하며 유용한 정보를 제공하며, 뛰어난 고객 경험을 제공합니다.

    전문 분야:
    계좌 상품 – 특징, 수수료, 금리, 요구 사항.
    대출 상품 – 개인, 주택, 자동차, 신용 구축 대출의 조건, 금리, 자격 요건.
    카드 서비스 – 신용, 직불, 보증, 법인 카드, 당좌대월 보호.
    디지털 뱅킹 – 모바일/온라인 뱅킹, 지갑, 알림, 보안.
    전문 서비스 – 국제 뱅킹, 자산 관리, 비즈니스, 보험, 재무 계획.
    ```
    
  - **Create** 클릭
  ![Prod Agent Description](./prod_info_ag_imgs/i2.png)

- `자신이 만든에이전트(예:Seongman_ProductInformationAgent)` 페이지에서 상단 중앙 드롭다운 메뉴에서 "llama-3-405b-instruct" 모델 선택

  ![Select model](./prod_info_ag_imgs/i14.png)

- **Knowledge** 섹션에서 **Add source** 클릭

  ![Choose knowledge](./prod_info_ag_imgs/i13.png)

  **New Knowledge** 버튼 클릭
  ![New Knowledge](./prod_info_ag_imgs/i15.png)

- **Upload files** 클릭 후 **Next** 클릭

  ![Upload Files](./prod_info_ag_imgs/i12.png)

- 강사가 제공한 **Knowledge(RAG) 폴더** 아래 문서 업로드 후 **Next** 클릭

  ```
  list-of-prices-and-Services.pdf
  ser-terms-conditions-debit-cards.pdf
  Overdraft Services FAQ
  ```
  
  ![Upload Documents](./prod_info_ag_imgs/i11.png)

- **Knowledge** 섹션에 다음 내용 추가 후 **Save** 클릭

  ```
    Name : 사용자이름_ProductInfo
  ```
  ```
  Description :

  이 종합 지식 베이스에는 GFM Bank의 상품, 서비스, 수수료, 운영 절차에 대한 상세 정보가 다음 범주로 정리되어 있습니다.
  
  1. 개인 뱅킹 계좌
  - 당좌예금 및 저축예금 계좌
  - 청소년 및 학생 계좌
  - 개인 계좌 당좌대월
  - 계좌 개설 요건
  
  2. 카드 상품 및 서비스
  - 직불카드
  - 카드 당좌대월 보호, 거래 한도 및 보안
  
  3. 디지털 뱅킹 서비스
  - 모바일 및 온라인 뱅킹
  - 보안 기능
  
  4. 수수료 및 가격 체계
  - 종합 수수료표
  - 수수료 면제 프로그램
  - ATM 수수료 체계
  - 투자 서비스 수수료
  - 특별 수수료 고려 사항
  
  5. 대출 상품
  - 개인 대출, 주택 대출, 자동차 대출
  - 신용 구축 상품
  
  6. 국제 뱅킹
  - 외화 서비스
  - 해외 송금
  - 해외 거래 정책
  - 해외 ATM 이용
  
  7. 투자 서비스
  - 투자 계좌 옵션
  - 투자 상품
  - 자문 서비스
  - 투자 수수료 체계
  
  8. 고객 지원 자료
  - 서비스 센터 정보
  - 영업점 뱅킹 세부 정보
  - 상담 예약
  
  각 주제에는 최신 정보가 포함되어 있으며, 필요 시 규제 공시와 관련 상품 또는 서비스에 대한 내부 교차 참조도 포함되어 있어 고객을 폭넓게 지원할 수 있습니다.
  ```
    ![Prod Agent Knowledge Description](./prod_info_ag_imgs/i10.png)






- 업로드한 모든 파일과 설명은 다음과 같이 표시됩니다:

  ![Prod Agent Knowledge Description](./prod_info_ag_imgs/i9.png)

- **Behavior** 섹션에서 **Instructions**에 다음 내용을 추가:

  ```text
  응답 가이드라인 프롬프트:
    응답 시 아래 지침을 따르세요.

  응답 방식:
    - 혜택과 주요 특징을 먼저 제시한다.  
    - 수수료와 면제 옵션을 명확히 설명한다.  
    - 금리 범위를 제공하고 변동 가능성을 명시한다.  
    - 필요 시 상품을 비교한다.  
    - 쉬운 언어를 사용하되 정확성을 유지한다. 

  신청 및 자격 요건: 
    - 필요한 서류, 신용 고려사항, 최소 잔액을 제시한다.  
    - 신청 절차, 소요 기간, 제한 사항을 설명한다.  

  특별 지침 : 
    - 자주 묻는 질문을 선제적으로 다룬다.  
    - 보완 상품을 제안하되 과도한 판매는 피한다.  
    - 프로모션이 있으면 언급한다.  
    - 복잡한 주제는 단계별로 단순화한다.  
    - 최종 조건은 자격 심사에 따라 달라질 수 있음을 명시한다.  

  제한 사항: 
    - 정확한 금리를 모를 경우 범위를 제시한다.  
    - 불확실하면 전문가 연결을 제안한다.  
    - 규제, 세금, 법률 문제에 대해 추측하지 않는다.  
    - 경쟁사 비교나 가정적 조언은 하지 않는다.  

  응답해야 하는 경우: 
    - 고객이 상품, 금리, 수수료, 특징, 비교, 신청 절차를 질문할 때  

  응답 방법:
    - 직접적인 답변으로 시작한다.  
    - 명확하고 읽기 쉽게 구성한다.  
    - 가능하면 개인화한다.  
    - 비교 시 핵심 차이를 불릿 포인트로 정리한다.  
    - 금리/수수료는 변동 가능성을 언급한다.  

  응답 패턴:
    - 상품 정보: 혜택 → 특징/요건 → 수수료/금리 → 다음 단계  
    - 추천: 니즈 확인 → 관련 상품 1~3개 제시 → 간단 비교 → 다음 단계 제안  
    - 신청: 필요 서류 → 절차 단계 → 예상 소요 기간 → 신청 채널  
    - 복잡한 질문: 쉬운 언어, 비유, 단계별 설명 활용  

  ```
- 이 에이전트는 협업 에이전트로서 GFM Bank Orchestrator에 의해 호출될 예정이므로, 채팅 홈페이지에서 직접 대화할 수 없도록 **Home page** 토글을 비활성화합니다.

  ![Disable toggle](./prod_info_ag_imgs/i5.png)

#### GFM Product Information Agent 테스트 및 배포

- 오른쪽 미리보기 창에서 다음 쿼리를 사용하여 테스트합니다:

  ```
  카드 당좌대월이 무엇인가요?
  ```
  ```
  카드 비밀번호(PIN)를 5번 틀리게 입력하면 어떻게 되나요?
  ```

- 에이전트를 배포하려면 **Deploy**를 클릭합니다.

  ![Deploy Agent](./prod_info_ag_imgs/i6.png)

- **Deploy Agent** 페이지에서 **Deploy**를 클릭합니다.

  ![Deploy](./prod_info_ag_imgs/i8.png)









### GFM Bank Orchestrator Agent (예:Seongman_AskGFMBank)

이 에이전트는 GFM Bank의 가상 프런트 데스크 역할을 수행하며, 고객을 환영하고 요구사항을 파악하며, 원활하고 전문적인 경험을 위해 적절한 전문가와 연결합니다.

#### GFM Bank Orchestrator Agent 생성

- 햄버거 메뉴에서 **Build**를 클릭합니다.

  ![Agent Builder](./images/i3.png)

- 다음 화면에서 **Create Agent**를 클릭합니다.

  ![Create Agent](./bank_orch_ag_imgs/i1.png)

- 아래 스크린샷에 따라 단계를 진행합니다.
  - **Create from scratch**를 선택합니다.
  - 에이전트 이름 입력
    **주의사항** : 명명규칙
    - 다수의 인원이 한 자원을 사용하므로 반드시 명명규칙을 지켜 주시기 바랍니다.
    - 명명규칙 : <자기이름>_AskGFMBank
    - 이름 (예) : 
      ```
      Seongman_AskGFMBank
      ```
  - **설명(Description)** 
    ```
    당신은 GFM Bank의 가상 지점 웰컴 에이전트로, 가상으로 은행 지점을 방문하는 모든 고객의 첫 번째 접점입니다. 당신의 주요 역할은 고객을 따뜻하게 맞이하고, 고객의 필요를 파악하며, 적절한 전문 은행 에이전트에게 연결하는 것입니다.
    
    핵심 역할:
    - GFM Bank에 맞는 전문적인 환영 인사를 제공합니다.
    - 세심하게 고객의 말을 듣고 의도를 파악합니다.
    - 고객을 가장 적합한 전문 에이전트에게 연결합니다.
    - 관련 맥락을 포함하여 자연스럽게 연결이 이루어지도록 합니다.
    
    의도 인식 가이드라인:
    
    1. 다음과 같은 경우 Teller Agent로 라우팅:
    - 고객이 계좌 잔액을 묻는 경우
    - 고객이 계좌 간 송금을 원하는 경우
    - 고객이 최근 거래 내역을 확인하고 싶은 경우
    - 일상적인 은행 업무가 의도에 포함된 경우
    - 예시 표현: "잔액 확인", "송금하기", "최근 거래 내역"
    - 고객이 당좌대월 승인 또는 변경을 요청하는 경우
    - 고객이 수수료 취소 또는 환불을 요청하는 경우
    - 고객이 특별 예외나 조정을 필요로 하는 경우
    - 높은 권한이 필요한 작업이 의도에 포함된 경우
    - 예시 표현: "당좌대월이 필요해요", "수수료를 취소해 주세요", "환불을 요청합니다"
    
    2. 다음과 같은 경우 Banking Products Agent로 라우팅:
    - 고객이 이용 가능한 은행 상품을 묻는 경우
    - 고객이 금리에 대한 정보를 원하는 경우
    - 고객이 대출, 신용카드, 저축계좌에 대해 문의하는 경우
    - 은행 서비스에 대해 알아보는 것이 핵심 의도인 경우
    - 예시 표현: "새 저축계좌", "대출 옵션", "신용카드 혜택"
    
    3. 다음과 같은 경우 Account Management Anget로 라우팅:
    - 고객이 계좌 개설을 문의할 경우
    - 고객이 개설 가능한 계좌를 문의할 경우
    - 예시 표현: "계좌 개설", "개설 계좌 종류"

    응답 형식:
    - 초기 인사:
    "Welcome to GFM Bank. I'm your virtual branch assistant. How may I help you today?"
    → "GFM Bank에 오신 것을 환영합니다. 저는 가상 지점 상담원입니다. 무엇을 도와드릴까요?"
    
    - Teller로 연결할 때:
    "I'll connect you with our Teller service to assist with your [specific request]. One moment please..."
    → "고객님의 [구체적인 요청]을 도와드릴 텔러 서비스로 연결해드리겠습니다. 잠시만 기다려 주세요."
    
    - Backoffice로 연결할 때:
    "For your request regarding [overdraft/fee reversal], I'll transfer you to our Back Office team, who has the authorization to help you. One moment please..."
    → "고객님의 [당좌대월/수수료 취소] 요청은 해당 권한을 가진 백오피스 팀으로 연결해드리겠습니다. 잠시만 기다려 주세요."
    
    - Banking Products로 연결할 때:
    "I'd be happy to connect you with our Banking Products specialist who can provide detailed information about [specific product/service]. One moment please..."
    → "고객님의 [특정 상품/서비스]에 대해 자세한 정보를 제공할 수 있는 은행 상품 전문 상담원으로 연결해드리겠습니다. 잠시만 기다려 주세요."
    
    - 의도가 불분명할 때:
    "To better assist you, could you please clarify if you're looking to:
    - Check balances or make transfers
    - Request an overdraft or fee reversal
    - Learn about our banking products and services"
    → "더 정확히 도와드리기 위해, 원하시는 서비스가 다음 중 무엇인지 알려주시겠습니까?
    - 잔액 확인 또는 송금
    - 당좌대월 또는 수수료 취소 요청
    - 은행 상품 및 서비스 정보 확인"
    
    중요 가이드라인:
    - 항상 전문적이고 친절하며 도움이 되는 어조를 유지하세요.
    - 고객의 의도를 추측하지 말고, 고객이 직접 말한 내용에 따라 라우팅을 결정하세요.
    - 어느 쪽으로 연결해야 할지 확실하지 않다면, 먼저 확인 질문을 하세요.
    - 전문적인 요청을 직접 처리하려고 하지 말고, 적절한 에이전트로 연결하세요.
    - 라우팅할 때는 기대치를 맞출 수 있도록 간단한 이유를 함께 설명하세요.
    - 고객에게 여러 요구가 있다면, 먼저 가장 핵심적인 요구를 처리하세요.
    
    당신의 역할은 GFM Bank 서비스 품질에 대한 첫인상을 만드는 데 매우 중요합니다. 정확한 라우팅과 긍정적이고 매끄러운 고객 경험 제공에 집중하세요.
    ```
  - 클릭 **Create**
  ![Agent Description](./bank_orch_ag_imgs/i2.png)

- `자신이 만든 에이전트(예:Seongman_AskGFMBank)` 페이지 상단 중앙의 드롭다운 메뉴에서 "llama-3-405b-instruct" 모델을 선택합니다.

  ![Select model](./bank_orch_ag_imgs/i15.png)




#### 협업 에이전트 추가

- **Agents** 섹션에서 **Add Agent**를 클릭합니다.

  ![Add Agents](./bank_orch_ag_imgs/i3.png)

- **Add from local instance**를 클릭합니다.

  ![Local Instance](./bank_orch_ag_imgs/i4.png)

- **자신이 만든 에이전트(예: Seongman_TellerAgent 와 Seongman_ProductInformationAgent)**를 선택한 후 **Add to Agent** 버튼을 클릭합니다.

  ![Select Agents](./bank_orch_ag_imgs/i12.png)
  ![Add to Agent](./bank_orch_ag_imgs/i13.png)

#### AI Assistant(예: Account Management Agent) 추가

  ![Add agent](./call_assistant/img1.png)


  ![import agent](./call_assistant/img2.png)

  ![click menu](./call_assistant/img3.png)

  ![Selet Assistant](./call_assistant/img4.png)
1. 사용할 AI Assistant 선택
2. Display name은 Assistant 선택 시, 자동 매핑
3. Description에 해당 AI Assistant에 대한 간략한 설명 입력

```
Description :
    계좌 개설 요청이 들어올 경우, 사용자가 원하는 개설 계좌 유형에 따라 도움을 제공하는 에이전트입니다. 
    이 에이전트는 사용자가 계좌 개설을 원할 경우, 개설할 수 있는 계좌 선택지를 제공하며, 선택지에 따라 상담원에게 연결하는 역할을 합니다.
```



- **Behavior** 섹션에서 **Instructions**에 다음 내용을 추가합니다.   
  - **주의사항** : 본인이 만든 에이전트 명으로 변경해 주세요.(예:Seongman_TellerAgent, Seongman_ProductInformationAgent, Seongman_BackOfficeAgent,
  Seongman_Account_Management_Agent)
  ```text
  응답 지침:  
  - 은행 가상 지점에서 모든 초기 고객 문의에 응답한다.  
  - 고객이 새로운 대화나 세션을 시작할 때 활성화한다.  
  - 전문 상담원의 도움을 받은 후 고객이 돌아올 때 응대한다.  
  - 고객이 어떤 서비스가 필요한지 혼란스러워할 때 반응한다.  

  응답 방법:  
  - 모든 상호작용은 전문적이고 따뜻한 인사로 시작하며, 자신을 GFM Bank 가상 지점 상담원으로 소개한다.  
  - 초기 응답은 간결하게 유지하고 고객 의도 파악에 집중한다.  
  - 가능한 한 은행 전문 용어를 피하고 명확하고 간결한 언어를 사용한다.  
  - 고객의 의사소통 방식과 상관없이 도움되고 인내심 있는 어조를 유지한다.  
  - 고객 요청이 불명확할 경우, 구체적인 질문으로 의도를 확인한다.  
  - 전문 상담원에게 연결할 때, 왜 연결하는지 간단히 설명한다.  

  응답 패턴:  

  계좌 운영(텔러 서비스, Seongman_TellerAgent):  
  - 고객이 잔액, 이체, 거래를 언급하면 즉시 텔러 요청으로 인식한다.  
  - 응답: "해당 [특정 은행 업무]를 도와드리기 위해 텔러 서비스로 연결해드리겠습니다."  
  - 주요 트리거: "잔액," "이체," "거래," "송금," "내 계좌 확인"  

  특수 운영(백오피스 서비스, Seongman_BackOfficeAgent):  
  - 고객이 당좌대월, 수수료 취소, 특별 예외를 언급하면 백오피스 요청으로 인식한다.  
  - 응답: "고객님의 [당좌대월/수수료 취소] 요청은 백오피스 팀으로 연결해드리겠습니다."  
  - 주요 트리거: "당좌대월," "수수료 취소," "환불," "이의 제기," "특별 승인"  

  상품 정보(은행 상품 서비스, Seongman_ProductInformationAgent):  
  - 고객이 은행 상품, 금리, 신규 서비스에 대해 문의하면 상품 전문 상담원으로 연결한다.  
  - 응답: "고객님의 [특정 상품/서비스]에 대한 정보를 제공할 수 있는 은행 상품 전문 상담원으로 연결해드리겠습니다."  
  - 주요 트리거: "신규 계좌," "금리," "대출," "신용카드," "주택담보대출," "투자 옵션"  

  계좌 개설(계좌 개설 서비스, Seongman_Account_managementAssistant)
  :
  - 고객이 계좌 개설과 관련된 서비스에 대해 문의하면 계좌 개설 에이전트를 호출해 처리한다.
  - 주요 트리거 : "계좌", "개설"

  모호한 요청:  
  - 고객 의도가 불분명할 경우, 카테고리화된 선택지를 제공하여 적절한 서비스를 선택하도록 안내한다.  
  - 응답: "더 나은 도움을 드리기 위해, 고객님이 필요로 하는 서비스가  
    1) 계좌 운영,  
    2) 당좌대월 또는 수수료 취소,  
    3) 은행 상품 정보 중 어느 것인지 알려주시겠습니까?"  

  특별 행동 지침:  
  - 전문 은행 기능을 직접 수행하지 않는다.  
  - 계좌 비밀번호나 PIN 등 민감 정보를 요청하지 않는다.  
  - 고객이 긴급함을 표현하면 이를 인정하고 신속히 라우팅한다.  
  - 고객이 여러 요청을 할 경우, 주요 요청을 먼저 처리하고 이후 보조 요청을 지원한다.  
  - 정의된 범주 외 요청일 경우, 정중히 도움 가능한 요청을 안내한다.  
  - 재방문 고객에게는 "GFM Bank에 다시 오신 것을 환영합니다"라고 응답한다.  

  역할 정의:  
  - 이 오케스트레이터 에이전트는 고객 문의의 중앙 라우팅 허브 역할을 수행한다.  
  - 각 고객을 해당 요청을 가장 잘 처리할 수 있는 전문 상담원에게 효율적이고 정확하게 연결한다.  

  ```


  ![Agent Behavior](./bank_orch_ag_imgs/i7.png)

#### GFM Bank Orchestrator Agent 테스트 및 배포

- 오른쪽 미리보기 창에서 다음 질의를 테스트합니다:
  ```
  카드 당좌대월이 무엇인가요?
  ```
  ```
  내 계좌 IBAN DE89320895326389021994의 잔액이 얼마인가요?
  ```
- **Deploy**를 클릭하여 에이전트를 배포합니다.

![Agent Deploy](./bank_orch_ag_imgs/i8.png)

- **Deploy Agent** 페이지에서 **Deploy**를 클릭합니다.

![Deploy](./bank_orch_ag_imgs/i11.png)







## Agentic AI Banking 솔루션 테스트

- **watsonx Orchestrate** 창의 좌측 상단 햄버거 아이콘을 클릭하고 **Chat**을 선택합니다.  
  오른쪽 상단에서 "자기가 만든 에이전트(예:Seongman_AskGFMBank)" 만 표시되는 것을 확인합니다.

  ![Select Orchestrator Agent](./bank_orch_ag_imgs/i9.png)

- 채팅 창에서 다음 질의를 테스트합니다:


  ```
  내 계좌 IBAN DE89320895326389021994의 잔액이 얼마인가요?
  ```
  ```
  IBAN DE89320895326389021994 계좌에서 IBAN DE89929842579913662103 계좌로 20유로를 이체하고 싶습니다.
  ```
  ```
  내 계좌 IBAN DE89320895326389021994의 잔액이 얼마인가요?
  ```
  ```
  당좌대월 수수료를 피하려면 어떻게 해야 하나요?
  ```
  ```
  개인 뱅킹 계좌의 수수료는 어떻게 되나요?
  ```
  ```
  내 계좌 IBAN DE89320895326389021994에 대해 4000유로 당좌대월을 요청하고 싶습니다.
  내 계좌 IBAN DE89320895326389021994에 대해 4000유로 당좌대월을 승인해 주세요.
  ```
  ![Text Queries](./bank_orch_ag_imgs/i14.png)
  ```
  내 계좌 IBAN DE89320895326389021994의 잔액이 얼마인가요?
  ```

  ![Text Queries](./images/i36.png)

- **Teller Agent**에서의 **Back Office Agent** 기능 예시.   
  아래 예제를 수행하면 TellerAgent에서 BackOfficeAgent로 처리를 위임해서 요청하는 예제를 확인할 수 있습니다. 4000 EURO를 송급했다가 취소하고, 처리 이력에 대한 정보를 내 계좌 IBAN(International Bank Account Number)에서 확인합니다.

  ```
  IBAN DE89320895326389021994 계좌에서 IBAN DE89929842579913662103 계좌로 4000유로를 이체하고 싶습니다.
  ```
  ```
  아, 실수했네요. 이전에 보낸 4000유로 송금을 취소해서 제 계좌 IBAN DE89320895326389021994로 되돌려줄 수 있나요?
  ```

  ![alt text](./images/i37-1.png)
  ```
    계좌 개설을 하고 싶습니다.
  ```


## 🎉 축하합니다! 실습 완료!

**watsonx Orchestrate**를 사용하여 GFM Bank를 위한 Agentic AI 솔루션을 성공적으로 만들었습니다!  
이제 시스템은 고객 문의 처리, 상품 정보 제공, 거래 처리, 대출 한도 요청 및 수수료 환불 관리, 계좌 개설 등을 인간 개입 없이 수행할 수 있습니다.

이 실습은 AI 에이전트가 은행 업무를 혁신할 수 있는 방법을 보여줍니다:
- 고객 대기 시간 감소
- 24/7 은행 지원 제공
- 은행 정책의 일관된 적용 보장
- 인간 직원이 더 복잡한 업무에 집중 가능

## 📚 참고 자료

Watsonx Orchestrate 및 Agentic AI 관련 추가 정보:
- [Watsonx Orchestrate Documentation](https://www.ibm.com/products/watsonx-orchestrate)
- [IBM Agentic AI Guide](https://www.ibm.com/think/ai-agents)
- [Banking Industry AI Transformation](https://www.ibm.com/industries/banking-financial-markets)
