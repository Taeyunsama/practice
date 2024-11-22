import streamlit as st
import pymysql as psql
import pandas as pd

Conn = psql.connect(user='root', passwd='ma29mi',host='localhost',db='insu',charset='utf8')

cursor = Conn.cursor(psql.cursors.DictCursor)

st.title('상품별 청구 금액 및 지급 금액 분석')
insurance = ['일반종신','일반연금','어린이','실손','보장','정기','일반CI','변액CI','변액종신','암','변액연금','어린이연금']
insurance = sorted(insurance)
name = st.selectbox("알아보고자 하는 보험명", insurance)
if name is not None:
    sql = "SELECT cntt.GOOD_CLSF_CDNM AS 상품명, cntt.SALE_CHNL_CODE AS 판매채널, \
    COUNT(DISTINCT cust.CUST_ID) AS 고객수, SUM(claim.DMND_AMT) AS 총청구금액, \
    SUM(claim.PAYM_AMT) AS 총지급금액, ROUND(AVG(claim.DMND_AMT), 2) AS 평균청구금액, \
    ROUND(AVG(claim.PAYM_AMT), 2) AS 평균지급금액, MAX(claim.DMND_AMT) AS 최대청구금액, \
    MAX(claim.PAYM_AMT) AS 최대지급금액, SUM(CASE WHEN cust.SEX = '1' THEN claim.DMND_AMT \
    ELSE 0 END) AS 남성청구금액, SUM(CASE WHEN cust.SEX = '2' THEN claim.DMND_AMT ELSE 0 END) AS 여성청구금액,\
    ROUND(SUM(claim.DMND_AMT) / COUNT(DISTINCT cust.CUST_ID), 2) AS 1인당평균청구금액, \
    ROUND(SUM(cust.CHLD_CNT * claim.DMND_AMT) / SUM(cust.CHLD_CNT), 2) AS 자녀1명당평균청구금액 \
    FROM Claim claim JOIN Cntt cntt ON claim.POLY_NO = cntt.POLY_NO JOIN Cust cust ON claim.CUST_ID = cust.CUST_ID \
    WHERE cntt.GOOD_CLSF_CDNM = '" + name + "'GROUP BY cntt.GOOD_CLSF_CDNM, cntt.SALE_CHNL_CODE ORDER BY 총청구금액 DESC, 총지급금액 DESC;"

    cursor.execute(sql)
    result = cursor.fetchall()
    result = pd.DataFrame(result)
    st.write(result)


st.title('직업군별 평균 청구 금액과 지급금액 비교')
job = ['주부','3차산업 종사자','사무직','2차산업 종사자','자영업','미상','학생','교육관련직','의료직 종사자','전문직','단순 사무직','운전직','고위 공무원','단순 노무직','공무원','1차산업 종사자','의료직 종사자','예체능계 종사자','교사','기업/단체 임원','종교인/역술인','대학교수/강사','학자/연구직','고소득의료직','고소득 전문직']
job = sorted(job)
name_2 = st.selectbox("직업군 선택", job)
if name_2 is not None:
    sql_2 = "SELECT cntt.GOOD_CLSF_CDNM AS 상품명, claim.ACCI_OCCP_GRP2 AS 사고직업군, \
    COUNT(DISTINCT claim.CLAIM_ID) AS 청구건수, AVG(claim.DMND_AMT) AS 평균청구금액, \
    AVG(claim.PAYM_AMT) AS 평균지급금액, ROUND(SUM(CASE WHEN claim.PAYM_AMT > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(claim.CLAIM_ID), 2) AS 지급비율\
    FROM Claim claim JOIN Cntt cntt ON claim.POLY_NO = cntt.POLY_NO \
	JOIN Cust cust ON claim.CUST_ID = cust.CUST_ID\
    WHERE cust.AGE >= 30 AND cust.AGE <= 50 AND claim.ACCI_OCCP_GRP2 = '" + name_2 + "' \
    GROUP BY cntt.GOOD_CLSF_CDNM, claim.ACCI_OCCP_GRP2\
    ORDER BY 청구건수 DESC, 지급비율 DESC; "
    cursor.execute(sql_2)
    result_2 = cursor.fetchall()
    result_2 = pd.DataFrame(result_2)
    st.write(result_2)
    
    