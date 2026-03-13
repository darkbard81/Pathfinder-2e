Phaser 기반 격자 + 자유 드래그 전술 퍼즐 게임 개발 로드맵

이 문서는 격자 기반이지만 유닛 이동은 자유롭고 충돌에 의해 동료 유닛 위치가 바뀌는 전술 퍼즐 RPG를 개발하기 위한 전체 개발 로드맵이다.

대상 기술 스택
	•	TypeScript
	•	Phaser
	•	Tile 기반 Grid 시스템
	•	Tween 애니메이션
	•	드래그 입력

⸻

0. 전체 개발 단계 개요

전체 개발은 다음 6단계로 진행한다.

1. 프로젝트 기반 구축
2. Grid 보드 시스템
3. 유닛 시스템
4. 드래그 이동 시스템
5. 충돌 및 밀림 시스템
6. 전투 및 협공 시스템
7. UI 및 게임 루프
8. 콘텐츠 제작
9. 최적화 및 배포


⸻

1. 프로젝트 기반 구축

목표

게임 실행 가능한 최소 구조 만들기

작업

Phaser 프로젝트 생성
Scene 구조 설계
기본 렌더 루프 구축

1단계 추천 확정 값 (프로젝트 초기 설정)

아래 값들은 Phaser 기반 격자 전술 퍼즐 게임을 만들기 위한 초기 프로젝트 설정 권장안이다.
각 항목에는 간단한 선택 이유를 포함한다.

Engine

Phaser 3 (Stable)

이유

플러그인과 예제가 대부분 Phaser 3 기준이며
Phaser 4는 아직 RC 단계라 실전 프로젝트 안정성이 낮음

Language

TypeScript

이유

유닛, 보드, 전투 시스템 등 객체 구조가 많기 때문에
타입 안정성이 유지보수와 개발 속도를 크게 높여줌

Build Tool

Vite

이유

빠른 개발 서버
간단한 설정
Phaser 공식 템플릿 존재
웹게임 개발에 매우 적합

Renderer

Phaser.AUTO

이유

가능하면 WebGL 사용
지원되지 않는 환경에서는 Canvas fallback
개발 초기에 가장 안정적인 선택

Base Resolution

1280 x 720

이유

16:9 기본 해상도
UI 배치가 편함
격자 보드 게임에 충분한 화면 공간

Aspect Ratio

16:9

이유

PC와 노트북 환경에서 가장 일반적인 비율
보드 기반 게임에 안정적인 화면 구성 가능

Scale Mode

FIT + CENTER_BOTH

이유

브라우저 크기에 맞춰 자동 확대
비율 유지
화면 중앙 정렬

Pixel Art Mode

pixelArt: true

이유

도트 그래픽에서 블러 방지
픽셀 선명도 유지

Physics Engine

Core Gameplay에서는 사용하지 않음

이유

이 게임의 이동과 충돌은
물리 충돌이 아니라 보드 규칙 기반 처리이기 때문

Scene 구성

BootScene
PreloadScene
TitleScene
GameScene
UIScene

이유

BootScene   → 엔진 초기 설정
PreloadScene → 에셋 로딩
TitleScene  → 메인 메뉴
GameScene   → 보드 / 유닛 / 전투 로직
UIScene     → HP, 버튼, 턴 정보 UI

Platform Target

Web First → Desktop Later

이유

웹에서 빠르게 테스트 가능
Electron / NW.js로 데스크톱 패키징 가능

Input Strategy

Mouse + Touch Drag

이유

유닛 이동이 드래그 기반
PC와 모바일 모두 대응 가능

폴더 구조

src
 ├ main.ts
 ├ game
 │   ├ Game.ts
 │   └ config.ts
 │
 ├ scene
 │   ├ BootScene.ts
 │   ├ PreloadScene.ts
 │   ├ TitleScene.ts
 │   └ GameScene.ts
 │
 └ assets

기본 Phaser 설정

const config: Phaser.Types.Core.GameConfig = {

  type: Phaser.AUTO,

  width: 1280,
  height: 720,

  scene: [
    BootScene,
    PreloadScene,
    TitleScene,
    GameScene
  ]

}


⸻

2. Grid 보드 시스템

목표

격자 기반 논리 좌표 시스템 구축

구현 기능

Grid 생성
Cell 좌표 관리
유닛 점유 상태 관리

데이터 구조

class Board {

  width:number
  height:number

  cells:(Unit | null)[][]

}

기능

placeUnit()
removeUnit()
getUnit()
moveUnit()


⸻

3. 유닛 시스템

목표

게임 캐릭터 데이터 관리

구조

Unit
 ├ gridPosition
 ├ renderPosition
 ├ sprite
 └ state

예시 코드

class Unit {

  gridX:number
  gridY:number

  sprite:Phaser.GameObjects.Sprite

}

기능

moveToCell()
playAnimation()
attack()


⸻

4. 드래그 이동 시스템

목표

유닛을 드래그로 이동

기능

유닛 선택
드래그 이동
현재 셀 계산
경로 추적

Phaser 입력

this.input.on("drag",(pointer,gameObject,x,y)=>{

  gameObject.x = x
  gameObject.y = y

})

좌표 변환

screen position → grid position

function screenToGrid(x:number,y:number){

  return {

    x: Math.floor(x / TILE_SIZE),
    y: Math.floor(y / TILE_SIZE)
  }

}


⸻

5. 충돌 및 밀림 시스템

목표

아군 유닛 충돌 시 위치 재배치

규칙

유닛 이동
→ 다른 유닛 발견
→ 밀림 처리
→ 연쇄 이동

예시

A → B → C

코드

function pushChain(board, unit, dx, dy){

  let x = unit.gridX + dx
  let y = unit.gridY + dy

  const chain = []

  while(board.getUnit(x,y)){

    chain.push(board.getUnit(x,y))

    x += dx
    y += dy
  }

  for(let i=chain.length-1;i>=0;i--){

    const u = chain[i]

    u.gridX += dx
    u.gridY += dy
  }

}


⸻

6. 애니메이션 시스템

목표

논리 이동을 자연스럽게 표현

방법

Tween animation

코드

scene.tweens.add({

  targets: unit.sprite,

  x: targetX,
  y: targetY,

  duration: 200

})


⸻

7. 전투 시스템

목표

협공 공격 구현

규칙

적을 양쪽에서 끼우면 공격

예시

A - Enemy - B

코드

function checkSandwich(board, enemy){

  const left = board.getUnit(enemy.x-1, enemy.y)
  const right = board.getUnit(enemy.x+1, enemy.y)

  if(left && right){
    return true
  }

}


⸻

8. UI 시스템

목표

게임 인터페이스 구성

구성

HP 바
스킬 UI
턴 표시
메뉴

구조

UIScene
 ├ health bar
 ├ skill buttons
 └ turn indicator


⸻

9. 이벤트 시스템

목표

스토리 및 컷신 처리

기능

대화 이벤트
스크립트 이벤트
카메라 연출

구조

EventSystem
 ├ dialogue
 ├ cutscene
 └ trigger


⸻

10. 콘텐츠 제작

제작 요소

맵 제작
적 데이터
스킬
아이템
퀘스트

데이터 구조

data
 ├ enemies.json
 ├ skills.json
 ├ items.json
 └ maps


⸻

11. 최적화

작업

렌더링 최적화
파티클 최적화
오브젝트 풀링
메모리 관리


⸻

12. 배포

플랫폼

Web
Steam
Mobile

빌드

webpack / vite
electron / nwjs


⸻

최종 아키텍처

Game
 │
 ├ Scene
 │   ├ TitleScene
 │   ├ GameScene
 │   └ UIScene
 │
 ├ Systems
 │   ├ BoardSystem
 │   ├ DragSystem
 │   ├ BattleSystem
 │   ├ AnimationSystem
 │   └ EventSystem
 │
 ├ Entities
 │   ├ Player
 │   ├ Enemy
 │   └ NPC
 │
 └ Data
     ├ Maps
     ├ Skills
     └ Items


⸻

최종 개발 순서

1. Phaser 프로젝트 생성
2. Grid 시스템 구현
3. 유닛 배치
4. 드래그 이동
5. 충돌 밀림
6. 애니메이션
7. 협공 공격
8. UI
9. 이벤트
10. 콘텐츠
11. 최적화
12. 배포


⸻

핵심 설계 철학

Grid = 게임 규칙

Render = 연출

두 시스템을 분리한다

이 구조를 사용하면 격자 기반 전술 퍼즐 RPG를 안정적으로 구현할 수 있다.