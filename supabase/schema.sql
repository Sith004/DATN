-- ==============================================================================
-- SUPABASE SCHEMA DEFINITION - ĐỒ ÁN TỐT NGHIỆP (NGUYỄN TRỌNG THỂ - 1150080117)
-- Đề tài: Nghiên cứu xây dựng mô hình Machine Learning trong đánh giá và dự báo
--         rủi ro tín dụng khách hàng.
-- ==============================================================================

-- 1. Tạo Schema credit_app nếu chưa có
CREATE SCHEMA IF NOT EXISTS credit_app;

-- 2. Phân quyền truy cập schema cho các role chuẩn của Supabase
GRANT USAGE ON SCHEMA credit_app TO postgres, anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA credit_app GRANT ALL ON TABLES TO postgres, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA credit_app GRANT ALL ON SEQUENCES TO postgres, service_role;

-- 3. Tạo bảng lưu trữ lịch sử dự báo rủi ro tín dụng
CREATE TABLE IF NOT EXISTS credit_app.customer_predictions (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Đặc trưng nhân khẩu học & hạn mức
    limit_bal NUMERIC NOT NULL,
    age INT NOT NULL,
    sex INT NOT NULL,
    education INT NOT NULL,
    marriage INT NOT NULL,
    
    -- Lịch sử thanh toán quá hạn 6 tháng gần nhất (PAY_0 .. PAY_6)
    pay_0 INT NOT NULL,
    pay_2 INT NOT NULL,
    pay_3 INT NOT NULL,
    pay_4 INT NOT NULL,
    pay_5 INT NOT NULL,
    pay_6 INT NOT NULL,
    
    -- Số dư hóa đơn hàng tháng (BILL_AMT1 .. BILL_AMT6)
    bill_amt1 NUMERIC NOT NULL,
    bill_amt2 NUMERIC NOT NULL,
    bill_amt3 NUMERIC NOT NULL,
    bill_amt4 NUMERIC NOT NULL,
    bill_amt5 NUMERIC NOT NULL,
    bill_amt6 NUMERIC NOT NULL,
    
    -- Số tiền đã thanh toán hàng tháng (PAY_AMT1 .. PAY_AMT6)
    pay_amt1 NUMERIC NOT NULL,
    pay_amt2 NUMERIC NOT NULL,
    pay_amt3 NUMERIC NOT NULL,
    pay_amt4 NUMERIC NOT NULL,
    pay_amt5 NUMERIC NOT NULL,
    pay_amt6 NUMERIC NOT NULL,
    
    -- Kết quả đánh giá & dự báo Machine Learning
    default_probability NUMERIC(6, 4) NOT NULL,
    prediction_label VARCHAR(50) NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    model_version VARCHAR(50) NOT NULL DEFAULT 'xgboost_tuned_v1',
    threshold NUMERIC(4, 2) NOT NULL DEFAULT 0.60,
    
    -- Các đặc trưng kỹ thuật số (33 features sau feature engineering)
    engineered_features JSONB
);

-- 4. Tạo các chỉ mục (Indexes) tối ưu hóa tốc độ truy vấn
CREATE INDEX IF NOT EXISTS idx_customer_predictions_created_at 
    ON credit_app.customer_predictions (created_at DESC);

CREATE INDEX IF NOT EXISTS idx_customer_predictions_risk_level 
    ON credit_app.customer_predictions (risk_level);

-- 5. Cấp quyền truy cập bảng
GRANT ALL PRIVILEGES ON TABLE credit_app.customer_predictions TO postgres, service_role;
GRANT SELECT ON TABLE credit_app.customer_predictions TO authenticated;
