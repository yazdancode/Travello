import React, { useState } from 'react';
import '../css/LoginForm.css'; // برای اضافه کردن استایل سفارشی

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    if (!username || !password) {
      setMessage('لطفاً تمام فیلدها را پر کنید.');
      return;
    }

    // در اینجا می‌توانید درخواست ورود به سرور را ارسال کنید
    setMessage('ورود با موفقیت انجام شد!');
  };

  return (
    <div className="login-container">
      <h1 className="login-title">سفرلو</h1>
      <form onSubmit={handleLogin} className="login-form">
        <div className="input-field">
          <label>نام کاربری</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="نام کاربری را وارد کنید"
          />
        </div>
        <div className="input-field">
          <label>رمز عبور</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="رمز عبور را وارد کنید"
          />
        </div>
        <button type="submit" className="login-button">
          وارد شوید
        </button>
      </form>
      {message && <p className="login-message">{message}</p>}
      <div className="login-footer">
        <a href="/register">ثبت‌نام کنید</a> | <a href="/about">درباره ما</a>
      </div>
    </div>
  );
};

export default LoginForm;
