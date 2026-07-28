"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
Dự án: Trợ Lý Tìm & Đặt Lịch Xem Nhà Trọ / Căn Hộ Cho Thuê
"""

import json
import os
import sys
from dotenv import load_dotenv

# Đảm bảo import các module cùng thư mục src/ hoạt động mượt mà
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# =====================================================================
# 🔗 LẮP RÁP CÁC MODULE (TỪ FILE CỦA ROLE 2 & 3)
# =====================================================================
# Xóa get_weather cũ, import AVAILABLE_TOOLS của dự án Nhà Trọ
from tools import AVAILABLE_TOOLS
from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, MAX_ITERATIONS
from providers import get_llm_provider

load_dotenv()

def load_test_cases():
    """Đọc bộ test cases từ config/test_cases.json của Role 1"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    
    if not os.path.exists(config_path):
        config_path = "test_cases.json"
        
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_baseline_chatbot(user_query: str, provider):
    """
    Dựng Chatbot gốc (Baseline) không có công cụ.
    Mục tiêu Mốc 2: Xem Chatbot phản ứng thế nào khi không có Tool tra cứu.
    """
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    print(f"⚙️ System Prompt đang dùng: (Ẩn để giao diện gọn gàng, xem trong code)")
    
    try:
        # Gọi LLM Provider thực hiện sinh câu trả lời
        response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
        print(f"🤖 Chatbot trả lời:\n{response}")
    except Exception as e:
        print(f"⚠️ Provider chưa được cấu hình (Thiếu API Key): {e}")
        print("🤖 Chatbot trả lời (Giả lập): Xin lỗi, tôi không có quyền truy cập cơ sở dữ liệu thời gian thực để tìm phòng trọ cho bạn lúc này.")


def run_react_agent(user_query: str, provider):
    """
    Dựng vòng lặp ReAct Agent (Thought -> Action -> Observation).
    Bản nháp chuẩn bị cho Mốc 3 - Gọi trực tiếp hàm thật từ Role 2.
    """
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")
    step = 0
    
    while step < MAX_ITERATIONS:
        step += 1
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")
        
        # GIẢ LẬP LOGIC CỦA AGENT CHO ĐÚNG ĐỀ TÀI TÌM NHÀ TRỌ (Sẽ nối LLM thật ở Mốc 3)
        if step == 1:
            print("🧠 Thought: Khách cần tìm phòng trọ dưới 4 triệu ở Cầu Giấy. Tôi sẽ gọi tool search_rentals.")
            print("🛠️ Action: search_rentals(location='Cau Giay', max_price=4000000, property_type='phong tro')")
            
            # Gọi thẳng tool thật từ file tools.py của Role 2 (bạn Kiệt) để minh họa
            obs = AVAILABLE_TOOLS["search_rentals"](location="Cau Giay", max_price=4000000, property_type="phong tro")
            print(f"👁️ Observation:\n{obs}")
            
        elif step == 2:
            print("🧠 Thought: Tôi đã có danh sách 2 phòng phù hợp. Giờ tôi sẽ báo lại cho khách.")
            print("🏁 Final Answer: Chào bạn, tôi tìm thấy 2 phòng trọ ở Cầu Giấy phù hợp với ngân sách dưới 4 triệu của bạn (Mã PT001 giá 3.5tr và Mã PT003 giá 3.8tr). Bạn muốn xem chi tiết mã phòng nào không?")
            break
            
    if step >= MAX_ITERATIONS:
        print(f"🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn tối đa {MAX_ITERATIONS} bước. Ngắt lặp an toàn!")


if __name__ == "__main__":
    print("==================================================")
    print("🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT")
    print("🚀 DỰ ÁN: TRỢ LÝ TÌM & ĐẶT LỊCH XEM NHÀ TRỌ")
    print("==================================================")
    
    # Khởi tạo Multi-Provider LLM Adapter
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")
    
    tests = load_test_cases()
    if tests:
        print(f"✅ Đã tải thành công {len(tests)} Test Cases từ file của Role 1\n")
        # Chạy thử câu test số 3 (id=3, index=2) - Multi-step (Cần Tool)
        sample_query = tests[2]["question"] 
    else:
        print("⚠️ Lỗi: Không tải được test_cases.json.")
        sample_query = "Tìm giúp tôi phòng trọ dưới 4 triệu/tháng ở quận Cầu Giấy, Hà Nội."
    
    print("--- DEMO 1: CHẠY TRÊN CHATBOT BASELINE (MỐC 2) ---")
    run_baseline_chatbot(sample_query, provider)
    
    print("\n--- DEMO 2: CHẠY TRÊN REACT AGENT (BẢN NHÁP CHO MỐC 3) ---")
    run_react_agent(sample_query, provider)