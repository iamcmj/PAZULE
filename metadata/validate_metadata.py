# ============================================
# metadata/validator.py
# ============================================
from metadata.metadata import quick_photo_summary


def validate_metadata(image_path):
    """
    사진 메타데이터 유효성 검사
    - 촬영일이 오늘인지
    - 지정된 BBox(출판단지) 내부인지
    둘 다 만족해야 True 반환
    """
    print("\n[STEP 1] Checking metadata...")
    try:
        result = quick_photo_summary(image_path)
        if not result:
            print("⚠️  메타데이터 검증 실패 (오늘 촬영 or 위치 조건 불만족)")
        return result
    except Exception as e:
        print(f"❌ Metadata validation failed: {e}")
        return False
