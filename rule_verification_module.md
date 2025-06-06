## 1. 규칙 검증 모듈 개념도

1. **질문 분석 단계**  
   - 사용자가 묻는 키워드(예: “킷순 Ability Boosts”, “클레릭 HP 계산” 등)를 먼저 파악  
   - 필요한 규칙 범위(Ancestry, Heritage, Background, Class, Free Boost 등) 대략적으로 추정  

2. **문서 검색(Verification) 단계**  
   - **file_search** 도구를 무조건 사용해, 질문과 관련된 구체적인 용어(예: “Kitsune Ability Boosts” 또는 “Field Medic ability boost”)를 **최소 1회 이상** 문서에 검색  
   - 검색 결과에서 “핵심 조문(text snippet)”을 찾아 인용(filecite…)  
   - 만약 동일한 주제에 대해 복수의 문서(LOAG, Core Rulebook, APG)를 참조해야 한다면 각 문서를 순차적으로 검색해서 결과를 병합  

3. **사실 확인(Fact Extraction) 단계**  
   - 검색 결과에서 나온 문구(페이지 번호, 표, 소제목)를 바탕으로 “정확히 어떤 단어/줄”이 해당 규칙을 명시하는지 확인  
   - 예:  
     - “Kitsune”에서 “Ability Boosts Charisma, Free”만 나오는지  
     - “Celestial Envoy Kitsune”에서 능력치 보정이 없는지  
     - “Field Medic” 배경 설명에서 능력치 부스트가 어떻게 나오는지  
   - 확인된 원문을 그대로 발췌하고, “해당 원문이 이렇다”는 사실을 1:1 대응으로 인용  

4. **내부 검토(Consistency Check) 단계**  
   - **문서 간 모순 여부**를 확인  
     - 만약 Core Rulebook과 Lost Omens Ancestry Guide가 같은 항목을 다르게 쓰고 있다면, 둘 다 인용한 뒤 “각 문헌에서 이렇게 서술하고 있다”를 투명하게 보고  
   - **이전 대화 기록과 충돌 여부**를 검사  
     - 만약 과거에 제가 잘못된 주장을 했다면(예: “킷순에 Flaw가 있다”), 그 대화 내용을 “참조”하되 바로잡은 근거(원문 인용)도 함께 제시  

5. **최종 답변 생성 단계**  
   - 위 단계를 거쳐 확보한 “절대 오류 없는 원문 인용”을 토대로  
     1. 사용자가 묻는 질문에 대한 단답형 요점  
     2. 그 뒤에 뒤따르는 “룰북 원문 퍼센티지 인용(filecite…)”  
     3. 필요하다면 간단한 해설(단순히 원문을 풀어서 설명)  
   - “추론”이나 “상식”은 일절 배제  
   - “만약 홈브루나 GM 재량 사항이라면, 공식 문헌에 없음을 명확히 밝히고 홈브루임을 한 문장으로 고지”

---

## 2. 구체적 지침(체크리스트)

1. **질문 키워드 도출**  
   - 사용자가 묻는 바가 “어떤 조문/어떤 페이지”에 있는지 빠르게 파악  
   - 예: “킷순 Ability Boosts” → LOAG p.121 “Kitsune” 표부터 검색  

2. **file_search 검색 수행**  
   - 키워드 문장 예시:  
     - `"Kitsune Ability Boosts"`  
     - `"Ability Flaw Kitsune"`  
     - `"Field Medic ability boost"`  
     - `"Cleric hit points calculation"`  
   - **꼭 1회 이상** 검색하고, 결과가 없더라도 “해당 키워드로 문서에서 아무것도 찾을 수 없었다”는 점을 보고  
   - “결과 없음”이라면 그 즉시 “문서 어디를 찾아봐도 이 용어(Ability Flaw)는 등장하지 않는다”고 정리  

3. **원문 발췌 및 인용**  
   - 검색 결과 중 적합한 부분을 식별한 뒤,  
     - “문장 전체” 또는 “표(표시된 Boost/Flaw) 전체”를 복사하듯이 발췌  
   - 인용형태:  
     ```
     > Ability Boosts
     >   Charisma
     >   Free
     ```
     와 같이 “원문 그대로” 옮기고, 페이지 번호 및 filecite… 형태로 표기  

4. **다른 문헌(유사 키워드) 재검색**  
   - 예: “‘Kitsune Ability Boosts’가 LOAG에 없으면, Core Rulebook에도 어딘가 더 있을 수 있으니 ‘Kitsune’ 키워드로 재검색”  
   - APG나 Secrets of Magic처럼, Ancestor/Heritage 관련 정보가 분산된 문서는 모두 한번 훑기  

5. **모순·누락 여부 확인**  
   - “만약 다른 문헌(예: APG)에서 킷순 관련 특별 예외 조항을 추가로 언급할 가능성”까지 검토  
   - 예: APG가 “특정 상황”에 Bloodline이나 Heritage 보너스 예외를 주는지 확인  
   - 모순이 발생하면 “이 두 문헌 내용이 이렇게 다르다”를 명확히 보고  

6. **최종 요약 문장 작성**  
   - 질문에 대한 1–2문장 결론 (예: “LOAG p.121 기준, Kitsune에는 Ability Flaw가 없으며, 오직 ‘Charisma +2, Free +2’만 적용됩니다.”)  
   - 그 뒤에 간단한 해설(“따라서 −WIS 결함은 공식 룰이 아닙니다. GM 홈브루로만 가능합니다.” 같은 짧은 문장)  

7. **인용·출처 정리**  
   - 답변말미에 사용한 모든 filecite… 출처를 정리  
   - “필요하다면 두 개 이상의 출처를 묶어서 표시” (예: fileciteturn21file0turn21file11)  

8. **내부 검토(Self-Review)**  
   - 작성된 답변을 훑으면서 “인용한 문장과 제가 쓴 설명이 1:1로 정확하게 대응되는지” 다시 확인  
   - “만약 설명 부분에 제가 헷갈리는 용어(Free Boost, Heritage 등)를 썼다면, 오류 발생 소지가 있으니 아예 지우거나 수정”  

9. **답변 제출 전 최종 확인**  
   - “문서에서 확인되지 않은 내용이 섞였는지” 다시 검토  
   - “과거 대화의 잘못된 주장(킷순 Flaw 등)이 슬쩍 섞이지 않았는지” 확인  

10. **자동화 가능 포인트**  
   - 위 과정을 최소화하기 위해, AI 내부에서 “질문 키워드 → file_search 쿼리 → 결과 파싱”을 반자동화하는 단계 구현  
   - “인용할 원문 발췌 → 인용 태그 자동 삽입” 로직을 AI 응답 텍스트 생성 모듈에 추가

---

## 3. 예시: “킷순 Ability Flaw” 검증 프로세스

1. **질문**: “킷순 Ancestry에 Ability Flaw가 있나요?”  
2. **키워드 도출**: `"Kitsune Ability Flaw"`  
3. **file_search** 수행:  
   ```json
   {"queries": ["Kitsune Ability Flaw", "Kitsune Ability Boosts Lost Omens Ancestry Guide p.121"]}
   ```  
4. **검색 결과**:  
   - LOAG p.121:  
     ```
     Ability Boosts
       Charisma
       Free

     Languages
       Common
       …  
     ```  
     (“Ability Flaw” 항목 없음) fileciteturn21file0  
   - APG, Core Rulebook에는 Kitsune 항목 자체가 없으므로 추가 검색 불필요  
5. **원문 인용**:  
   ```
   > Ability Boosts
   >   Charisma
   >   Free
   ```  
   fileciteturn21file0  
6. **결론 작성**:  
   - “LOAG p.121 기준, 킷순에는 ‘Ability Flaw: Wisdom’이 존재하지 않습니다. 오직 ‘Charisma +2’와 ‘Free +2’만 적용됩니다.”  
7. **인용·출처**: fileciteturn21file0  
8. **검토**: “문장과 인용이 정확히 맞는지 확인”  
9. **완료**: 사용자에게 제출

---

## 4. 요약

- **“문서 검색 → 원문 인용 → 자체 검토”** 과정을 **무조건 거치기**  
- **추론이나 기억 대신, 매번 실시간으로 file_search 조회**  
- **검증되지 않은 정보는 절대로 답변에 넣지 않기**  
- **모순 발생 시, 두 출처를 모두 인용하고 차이점만 간단히 보고**  
- **답변 전 내부 Self-Review** 단계로 마지막 확인  

이 절차를 철저히 따르면 “거짓말”이나 “추론의 오류” 없이, 언제나 “룰북 원문”에 기반해 정확한 답변만을 드릴 수 있습니다. 앞으로는 위 모듈과 체크리스트를 반드시 준수하여 혼선 없는, 신뢰 가능한 응답을 제공하겠습니다.
