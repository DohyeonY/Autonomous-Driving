import React, { useEffect, useState } from "react";
import HomeBanner1 from "./HomeBanner1";
import HomeBanner2 from "./HomeBanner2";
import BottomNav from "../../components/Nav/BottomNav";
import TopNav from "../../components/Nav/TopNav";
import styles from "./Home.module.css";
import { useNavigate } from "react-router-dom";
import ProductItem from "../../components/Product/ProductItem";
import axios from "axios";
import { useInView } from "react-intersection-observer";
import { useLocation } from "react-router";


// swiper - 이미지 슬라이더
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import {Autoplay} from 'swiper';

export default function Home() {
  const location = useLocation();
  const curLocation = location.pathname;

  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [page, setPage] = useState(0); // 현재 페이지 번호 (페이지네이션)
  const [ref, inView] = useInView();

  // 무한 스크롤
  // 지정한 타겟 div가 화면에 보일 때 마다 서버에 요청을 보냄
  const productFetch = () => {
    axios
      .get(
        `${process.env.REACT_APP_API_URL}/products/main?pageNo=${page}&pageSize=5`
      )
      .then((res) => {
        // 리스트 뒤로 붙여주기
        setProducts([...products, ...res.data]);
        // get으로 받은 데이터의 길이가 백에서 보내주기로 한 리스트보다 짧으면(?)
        // 불러온 데이터가 존재하기만 하면 다음 페이지로 처리 == 데이터가 0개 이면 마지막 현재 페이지를 마지막 페이지로
        if (res.data.length) {
          setPage((page) => page + 1);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  };

  useEffect(() => {
    // 타겟이 눈에 보이면 다음 페이지 요청하기
    if (inView) {
      productFetch();
    }
  }, [inView]);

  const clickProduct = (id) => {
    navigate(`/detail/${id}`);
  };

  return (
    <div className={styles.background}>
          <HomeBanner1 />


      <div className={styles.body}>
        <div className={styles.onsale}>판매중</div>
        <div className={styles.items}>
          {products?.map((product) => {
            return (
              <ProductItem
                key={product.productId}
                product={product}
                clickProduct={clickProduct}
              />
            );
          })}
          <div ref={ref} className={styles.ref}></div>
        </div>
        <BottomNav curLocation={curLocation} />
      </div>
    </div>
  );
}
