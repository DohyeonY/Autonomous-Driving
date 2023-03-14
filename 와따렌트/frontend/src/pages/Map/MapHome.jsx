import React from "react";
import { useNavigate } from "react-router-dom";
import styles from "./MapHome.module.css";
import GpsPage from "./GpsPage";

export default function MapHome() {
  const id = window.localStorage.getItem("loginId");
  const navigate = useNavigate();

  return (
    <div className={styles.background}>
      <div className={styles.body1}>
        <div className={styles.topleft}>
          <div className={styles.text}>
            <button
              onClick={() => {
                { navigate("/");}
              }}
            >
              HOME
            </button>
          </div>
          <div className={styles.texta}>{id}님 안녕하세요</div>
        </div>
        <div className={styles.textb}>어디로 갈까요?</div>
        <div className={styles.body2}>
        <GpsPage />
        </div>
      </div>
    </div>
  );
}
