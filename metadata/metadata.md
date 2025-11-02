# 📸 HEIC/JPG 메타데이터 기반 이미지 검증 시스템

파주 지역 촬영 사진의 메타데이터(EXIF)를 기반으로  
**촬영 시각·GPS 좌표·BBox(위치 유효성)** 를 검증하는 Python 유틸리티입니다.

---

## 주요 기능

### ✅ 3단계 검증 절차

1. **촬영 시각 검증**
   - EXIF 태그(`DateTimeOriginal`) 추출
   - 오늘 촬영 여부(`✅ PASS / ❌ NON PASS`) 판단

2. **GPS 좌표 추출**
   - HEIC/JPG 파일의 GPS IFD에서 위도(latitude), 경도(longitude) 추출
   - DMS(Degree, Minute, Second) → 십진수로 자동 변환

3. **BBox(경계 박스) 판정**
   - 사전에 정의된 위도/경도 범위 내에 있는지 확인
   - 지도 링크 자동 생성 (Google Maps)

---

## 지원 포맷

| 확장자 | 설명 | 지원 여부 |
|---------|------|------------|
| `.heic` | iPhone 촬영 기본 포맷 (HEIF) | ✅ |
| `.jpg` / `.jpeg` | 표준 JPEG 이미지 | ✅ |
| `.png` | 메타데이터 미보존, 분석 불가 | ⚠️ 제한적 |
| 기타 (`.gif`, `.bmp`) | EXIF 미지원 | ❌ |

---

## 지원 환경

✅ **Python 3.10 이상**  
✅ **Windows / macOS / Linux (Ubuntu 20.04+)**

---

## 설치

```bash
pip install pillow pillow-heif
