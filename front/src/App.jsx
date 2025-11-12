import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("mission");
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [missionType, setMissionType] = useState("photo");
  const [status, setStatus] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [todayHint, setTodayHint] = useState("");
  const [hintLoading, setHintLoading] = useState(true);

  const API_ENDPOINT = "http://localhost:8080";

  const missionTypes = [
    { 
      value: "photo", 
      label: "감성 촬영", 
      description: "감정이 담긴 사진을 찍어 업로드하세요",
      icon: "📷"
    },
    { 
      value: "location", 
      label: "장소 촬영", 
      description: "구조물이 있는 장소를 찾아가세요",
      icon: "📍"
    },
  ];

  // ✅ 서버에서 오늘의 힌트 가져오기 (mission_type에 따라)
  useEffect(() => {
    const fetchTodayHint = async () => {
      try {
        setHintLoading(true);
        // mission_type에 따라 다른 힌트 가져오기
        // "photo" -> missions2, "location" -> missions1
        const missionParam = missionType === "photo" ? "photo" : "location";
        const response = await fetch(`${API_ENDPOINT}/get-today-hint?mission_type=${missionParam}`);
        if (response.ok) {
          const data = await response.json();
          setTodayHint(data.hint || "");
        } else {
          console.error("힌트 가져오기 실패");
          setTodayHint("힌트를 불러올 수 없습니다.");
        }
      } catch (err) {
        console.error("힌트 가져오기 오류:", err);
        setTodayHint("힌트를 불러올 수 없습니다.");
      } finally {
        setHintLoading(false);
      }
    };

    fetchTodayHint();
  }, [missionType]); // missionType이 변경될 때마다 힌트 다시 가져오기

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setResult(null);
    
    // HEIC 파일 감지 (확장자 확인)
    const fileName = file.name.toLowerCase();
    const isHeic = fileName.endsWith('.heic') || fileName.endsWith('.heif');
    
    // 파일을 state에 저장 (서버로 전송할 파일)
    setImage(file);
    
    // HEIC/HEIF 파일인 경우 서버에서 변환된 미리보기 가져오기
    if (isHeic) {
      try {
        console.log('HEIC/HEIF 파일 감지, 서버에서 미리보기 변환 중...');
        
        // 서버로 HEIC 파일 전송하여 JPG로 변환된 미리보기 받기
        const formData = new FormData();
        formData.append("image", file);
        
        const response = await fetch(`${API_ENDPOINT}/api/preview`, {
          method: "POST",
          body: formData,
        });
        
        if (response.ok) {
          const blob = await response.blob();
          const reader = new FileReader();
          reader.onload = () => setPreview(reader.result);
          reader.readAsDataURL(blob);
          console.log('HEIC/HEIF → JPG 미리보기 변환 완료');
        } else {
          throw new Error('서버 변환 실패');
        }
      } catch (error) {
        console.error('HEIC 미리보기 변환 실패:', error);
        // 변환 실패 시 기본 이미지 아이콘 표시
        setPreview(null);
        // 파일은 그대로 유지 (서버에서 처리 가능)
      }
    } else {
      // 일반 이미지 파일 (JPEG, PNG 등) - 직접 미리보기
      const reader = new FileReader();
      reader.onload = () => setPreview(reader.result);
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async () => {
    if (!image) {
      alert("이미지를 선택해주세요.");
      return;
    }
    if (!missionType) {
      alert("미션 타입을 선택해주세요.");
      return;
    }

    setLoading(true);
    setStatus("미션 진행 중...");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("image", image);
      formData.append("mission_type", missionType);

      const response = await fetch(`${API_ENDPOINT}/api/mission`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        // 서버에서 반환한 에러 메시지 사용
        throw new Error(data.error || `서버 오류: ${response.status}`);
      }

      setStatus("완료!");
      setResult(data);
    } catch (err) {
      // 서버에서 반환한 에러 메시지를 그대로 표시
      setStatus(err.message);
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setImage(null);
    setPreview(null);
    setMissionType("photo");
    setStatus("");
    setResult(null);
    setLoading(false);
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) fileInput.value = "";
  };

  // 트로피 아이콘 SVG
  const TrophyIcon = () => (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M6 9H4C2.89543 9 2 9.89543 2 11V13C2 14.1046 2.89543 15 4 15H6M18 9H20C21.1046 9 22 9.89543 22 11V13C22 14.1046 21.1046 15 20 15H18M6 15V19C6 20.1046 6.89543 21 8 21H16C17.1046 21 18 20.1046 18 19V15M6 15H18M12 5V2M12 2L9 5M12 2L15 5M12 5C9.79086 5 8 6.79086 8 9V11C8 12.1046 8.89543 13 10 13H14C15.1046 13 16 12.1046 16 11V9C16 6.79086 14.2091 5 12 5Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );

  // 별 아이콘 SVG
  const StarIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
    </svg>
  );

  // 전구 아이콘 SVG
  const BulbIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M9 21H15M12 3C8.68629 3 6 5.68629 6 9C6 11.0929 7.20207 12.8945 9 13.8681V17C9 17.5523 9.44772 18 10 18H14C14.5523 18 15 17.5523 15 17V13.8681C16.7979 12.8945 18 11.0929 18 9C18 5.68629 15.3137 3 12 3Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );

  return (
    <div className="app-container">
      <div className="mission-container">
        {/* 헤더 */}
        <div className="header">
          <div className="trophy-icon">
            <TrophyIcon />
          </div>
          <h1 className="title">오늘의 미션</h1>
          <p className="subtitle">키워드를 찾아 미션을 완료하고 쿠폰을 받으세요!</p>
        </div>

        {/* 탭 네비게이션 */}
        <div className="tab-navigation">
          <button
            className={`tab-btn ${activeTab === "mission" ? "active" : ""}`}
            onClick={() => setActiveTab("mission")}
          >
            미션
          </button>
          <button
            className={`tab-btn ${activeTab === "history" ? "active" : ""}`}
            onClick={() => setActiveTab("history")}
          >
            히스토리
          </button>
        </div>

        {activeTab === "mission" && (
          <>
            {/* 미션 타입 선택 */}
            <div className="mission-type-section">
              <label className="label">미션 타입 선택</label>
              <div className="mission-type-cards">
                {missionTypes.map((type) => (
                  <div
                    key={type.value}
                    className={`mission-type-card ${missionType === type.value ? "active" : ""}`}
                    onClick={() => setMissionType(type.value)}
                  >
                    <div className="mission-type-header">
                      <span className="mission-type-icon">{type.icon}</span>
                      <span className="mission-type-label">{type.label}</span>
                      {missionType === type.value && <span className="selected-dot"></span>}
                    </div>
                    <p className="mission-type-description">{type.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* 오늘의 힌트 */}
            <div className="keyword-section">
              <div className="hint-section">
                <BulbIcon />
                <span className="hint-label">오늘의 힌트</span>
              </div>
              <p className="hint-text">
                {hintLoading ? "힌트를 불러오는 중..." : todayHint || "힌트를 불러올 수 없습니다."}
              </p>
            </div>

            {/* 이미지 업로드 */}
            <div className="upload-section">
              <label className="label">이미지 업로드</label>
              {preview ? (
                <div className="image-preview-container">
                  <img src={preview} alt="미리보기" className="preview-image" />
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="file-input"
                    id="image-upload"
                    disabled={loading}
                  />
                  <label htmlFor="image-upload" className="change-image-btn">
                    다른 이미지 선택
                  </label>
                </div>
              ) : (
                <div className="upload-area">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="file-input"
                    id="image-upload"
                    disabled={loading}
                  />
                  <label htmlFor="image-upload" className="file-input-label">
                    이미지 선택
                  </label>
                </div>
              )}
            </div>

            {/* 미션 제출 버튼 */}
            <button
              className="submit-btn"
              onClick={handleSubmit}
              disabled={!image || !missionType || loading}
            >
              {loading ? "처리 중..." : "미션 제출하기"}
            </button>

            {/* 상태 메시지 */}
            {status && (
              <div className={`status-message ${loading ? "loading" : ""}`}>
                {status}
              </div>
            )}

            {/* 결과 표시 */}
            {result && (
              <div className={`result-container ${result.success ? "success" : "fail"}`}>
                {result.success ? (
                  <div className="result-success">
                    <h2>🎉 미션 성공!</h2>
                    <div className="coupon-section">
                      <h3>쿠폰 지급</h3>
                      <div className="coupon-box">
                        {result.coupon ? (
                          <div>
                            <p className="coupon-code">{result.coupon.code || result.coupon}</p>
                            {result.coupon.description && (
                              <p className="coupon-description">{result.coupon.description}</p>
                            )}
                          </div>
                        ) : (
                          <p>쿠폰이 지급되었습니다!</p>
                        )}
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="result-fail">
                    <h2>😔 미션 실패</h2>
                    <div className="hint-section-result">
                      <h3>힌트</h3>
                      <div className="hint-box">
                        <p>{result.hint || "다시 시도해보세요!"}</p>
                      </div>
                    </div>
                  </div>
                )}
                {result.message && (
                  <p className="result-message">{result.message}</p>
                )}
              </div>
            )}
          </>
        )}

        {activeTab === "history" && (
          <div className="history-section">
            <p>히스토리 기능은 준비 중입니다.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
