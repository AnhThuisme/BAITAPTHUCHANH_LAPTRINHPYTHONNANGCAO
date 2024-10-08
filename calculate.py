def calculate_bmi(gender, spin_height, spin_weight, spin_age, lbl_result):
    try:
        height = float(spin_height.get())
        weight = float(spin_weight.get())
        age = int(spin_age.get())

        if height <= 0 or weight <= 0 or age <= 0:
            lbl_result.config(text="Lỗi: Chiều cao, cân nặng và tuổi phải lớn hơn 0!")
            return

        # Tính toán BMI
        bmi = weight / (height ** 2)
        result_text = f"BMI của bạn là: {bmi:.3f}\n"
        
        # Đánh giá tình trạng sức khỏe
        if gender == "Nam":
            if bmi < 18.5:
                result_text += "Bạn đang dưới chuẩn (gầy)."
            elif 18.5 <= bmi < 24.9:
                result_text += "Bạn có cân nặng bình thường."
            elif 25 <= bmi < 29.9:
                result_text += "Bạn đang thừa cân."
            else:
                result_text += "Bạn đang béo phì."
        else:  # Nữ
            if bmi < 18.0:
                result_text += "Bạn đang dưới chuẩn (gầy)."
            elif 18.0 <= bmi < 24.0:
                result_text += "Bạn có cân nặng bình thường."
            elif 24.0 <= bmi < 29.0:
                result_text += "Bạn đang thừa cân."
            else:
                result_text += "Bạn đang béo phì."
        
        # Cập nhật kết quả lên nhãn
        lbl_result.config(text=result_text)

    except ValueError:
        lbl_result.config(text="Lỗi: Vui lòng nhập đúng định dạng số!")