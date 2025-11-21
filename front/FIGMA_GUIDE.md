# Figma 디자인 적용 가이드

## 📍 파일 위치

Figma 디자인을 적용할 때 수정해야 할 파일들:

1. **스타일 파일**: `src/App.css` - 메인 스타일
2. **컴포넌트 파일**: `src/App.jsx` - HTML 구조
3. **글로벌 스타일**: `src/index.css` - 전체 스타일 (폰트, 기본 스타일 등)

## 🎨 적용 방법

### 방법 1: Figma에서 CSS 직접 추출

1. **Figma에서 CSS 추출**
   - 요소 선택 → 우측 패널에서 "Code" 탭 클릭
   - CSS 코드 복사

2. **App.css에 적용**
   - `src/App.css` 파일 열기
   - 해당 클래스에 Figma에서 추출한 CSS 적용

### 방법 2: 수동으로 값 변환

1. **Figma에서 값 확인**
   - 색상: `#FFFFFF` → CSS에 그대로 사용
   - 폰트 크기: `24px` → `font-size: 24px`
   - 간격: `16px` → `padding: 16px` 또는 `margin: 16px`
   - Border radius: `8px` → `border-radius: 8px`

2. **App.jsx에서 클래스명 확인**
   - 각 요소의 `className` 확인
   - `src/App.css`에서 해당 클래스 수정

### 방법 3: Figma 플러그인 사용

1. **Figma to Code 플러그인 설치**
   - Figma → Plugins → Browse plugins
   - "Figma to React" 또는 "html.to.design" 검색

2. **코드 생성**
   - 플러그인으로 React 코드 생성
   - 생성된 코드를 `src/App.jsx`와 `src/App.css`에 적용

## 📂 현재 프로젝트 구조

```
src/
  ├── App.jsx       ← HTML 구조 (여기서 className 확인)
  ├── App.css       ← 스타일 (여기서 디자인 적용)
  └── index.css     ← 글로벌 스타일 (폰트, 기본 스타일)
```

## 🔍 주요 클래스명 매핑

| Figma 요소 | CSS 클래스명 | 위치 |
|-----------|-------------|------|
| 메인 컨테이너 | `.app-container` | App.css |
| 미션 컨테이너 | `.mission-container` | App.css |
| 제목 | `.title` | App.css |
| 부제목 | `.subtitle` | App.css |
| 미션 타입 버튼 | `.mission-type-btn` | App.css |
| 업로드 영역 | `.upload-area` | App.css |
| 제출 버튼 | `.submit-btn` | App.css |
| 결과 컨테이너 | `.result-container` | App.css |

## 💡 예시: 버튼 스타일 변경

Figma에서 버튼 디자인을 가져왔다면:

```css
/* src/App.css */
.submit-btn {
  /* Figma에서 가져온 값들 */
  background-color: #667eea;  /* Figma 색상 */
  padding: 16px 32px;          /* Figma 간격 */
  border-radius: 8px;          /* Figma border radius */
  font-size: 16px;             /* Figma 폰트 크기 */
}
```

## 🚀 빠른 적용 팁

1. **Figma Dev Mode 사용** (유료)
   - Figma Dev Mode에서 CSS 코드 바로 확인
   - 복사해서 바로 적용 가능

2. **컴포넌트별로 나눠서 작업**
   - 버튼 스타일 → `.submit-btn` 수정
   - 카드 스타일 → `.mission-container` 수정
   - 입력 필드 → `.upload-area` 수정

3. **반응형 확인**
   - 모바일/태블릿/데스크톱 디자인이 있다면
   - `@media` 쿼리로 추가

## ❓ 질문이 있으면?

Figma 디자인을 완성하신 후:
1. 스크린샷 또는 Figma 링크 공유
2. 어떤 부분을 수정할지 알려주시면
3. 직접 코드로 변환해드릴 수 있습니다!

