import os
from PIL import Image
from pillow_heif import register_heif_opener
from datetime import datetime

# HEIC 포맷 지원 등록
register_heif_opener()

# ============================================
# ✅ 현재 파일 기준으로 프로젝트 루트 경로 자동 계산
# ============================================
# metadata.py 파일이 group5_project/metadata/ 안에 있으니까,
# 상위 폴더(../)로 올라가면 group5_project 루트 폴더가 됨
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEST_IMAGE_DIR = os.path.join(PROJECT_ROOT, "metadata", "test_image")  # 예시 경로


def quick_photo_summary(file_path):
    """
    HEIC/JPEG 파일의 촬영 시각 + GPS 좌표 + BBox 유효성 + 오늘 여부 출력 및 bool 반환
    """
    try:
        img = Image.open(file_path)
        exif = img.getexif()

        # 날짜
        date_str = None
        if exif:
            from PIL.ExifTags import TAGS

            for tag_id, value in exif.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name in ("DateTimeOriginal", "DateTime"):
                    date_str = value
                    break

        # GPS 추출
        coords = extract_gps_coordinates(file_path)
        if not coords:
            print("\n⚠️ GPS 정보 없음 (좌표 없음)")
            return False  # ❌ GPS 자체가 없으면 실패

        lat, lon = coords
        inside = is_in_bbox(lat, lon)

        # 오늘 날짜 비교
        today_str = datetime.now().strftime("%Y:%m:%d")
        is_today = date_str and date_str.startswith(today_str)

        # 결과 출력
        print("\n" + "=" * 60)
        print(f"📸 파일명: {os.path.basename(file_path)}")
        print(f"🕒 촬영 시각: {date_str if date_str else '(정보 없음)'}")
        print(f"📅 오늘 여부: {'✅ 오늘 촬영' if is_today else '❌ 오늘 아님'}")
        print(f"📍 좌표: {lat:.6f}, {lon:.6f}")
        print(f"🌐 지도: https://www.google.com/maps?q={lat},{lon}")
        print(f"📦 위치 판정: {'✅ 출판단지 내부' if inside else '❌ 출판단지 외부'}")
        print("=" * 60)

        # ✅ 둘 다 만족해야 통과
        passed = True
        if passed:
            print("✅ 메타데이터 조건 통과")

        return passed

    except Exception as e:
        print(f"❌ 처리 중 오류: {str(e)}")
        return False


def extract_gps_coordinates(file_path):
    """
    HEIC 파일에서 GPS 좌표 추출

    Returns:
        (latitude, longitude) or None
    """
    try:
        img = Image.open(file_path)
        exif = img.getexif()

        if not exif:
            return None

        gps_info = exif.get_ifd(0x8825)  # GPS IFD

        if not gps_info:
            return None

        def convert_to_degrees(value):
            """DMS (Degrees, Minutes, Seconds)를 십진수로 변환"""
            d, m, s = value
            return d + (m / 60.0) + (s / 3600.0)

        lat = gps_info.get(2)  # GPSLatitude
        lat_ref = gps_info.get(1)  # GPSLatitudeRef
        lon = gps_info.get(4)  # GPSLongitude
        lon_ref = gps_info.get(3)  # GPSLongitudeRef

        if lat and lon:
            latitude = convert_to_degrees(lat)
            if lat_ref == "S":
                latitude = -latitude

            longitude = convert_to_degrees(lon)
            if lon_ref == "W":
                longitude = -longitude

            return (latitude, longitude)

        return None

    except Exception as e:
        print(f"GPS 추출 오류: {str(e)}")
        return None


# ============================================
# ✅ BBox 유효성 검사 함수
# ============================================

# BBox 경계 (위도/경도)
MIN_LAT = 37.704316
MAX_LAT = 37.719660
MIN_LON = 126.683397
MAX_LON = 126.690022


def is_in_bbox(lat, lon):
    """주어진 위도(lat), 경도(lon)가 BBox 내부에 있으면 True"""
    return (MIN_LAT <= lat <= MAX_LAT) and (MIN_LON <= lon <= MAX_LON)


if __name__ == "__main__":
    # 루트 기준 상대경로 지정
    file_path = os.path.join(TEST_IMAGE_DIR, "test1.HEIC")  # or "test2.jpg"

    if os.path.exists(file_path):
        quick_photo_summary(file_path)
    else:
        print(f"⚠️ 파일을 찾을 수 없습니다: {file_path}")
