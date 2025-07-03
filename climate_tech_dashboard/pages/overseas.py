import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import numpy as np
import math
from pathlib import Path

# 페이지 설정
st.set_page_config(page_title="해외진출 현황", page_icon="🌏", layout="wide")

# CSS 스타일
st.markdown("""
<style>
    .overseas-card {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .region-card {
        background-color: #f0fff0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4ecdc4;
        margin: 0.5rem 0;
    }
    .top7-item {
        background-color: #ffffff;
        padding: 0.8rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.3rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_overseas_data():
    """해외진출 데이터 로드 또는 생성"""
    try:
        data_path = Path('./assets/data/processed/overseas_data.csv')
        if data_path.exists():
            return pd.read_csv(data_path)
        else:
            return create_sample_overseas_data()
    except Exception as e:
        st.error(f"해외진출 데이터 로드 실패: {str(e)}")
        return create_sample_overseas_data()

def create_sample_overseas_data():
    """샘플 해외진출 데이터 생성"""
    np.random.seed(42)
    
    # 지역별 좌표 정보
    regions_info = {
        '동남아시아': {
            'countries': ['베트남', '태국', '인도네시아', '필리핀', '말레이시아'],
            'lat': 10.0, 'lon': 110.0, 'weight': 1.5
        },
        '중국': {
            'countries': ['중국'],
            'lat': 35.0, 'lon': 104.0, 'weight': 2.0
        },
        '일본': {
            'countries': ['일본'],
            'lat': 36.0, 'lon': 138.0, 'weight': 1.2
        },
        '중동': {
            'countries': ['UAE', '사우디아라비아', '카타르'],
            'lat': 25.0, 'lon': 45.0, 'weight': 1.8
        },
        '유럽': {
            'countries': ['독일', '프랑스', '영국', '네덜란드'],
            'lat': 54.0, 'lon': 15.0, 'weight': 1.3
        },
        '북미': {
            'countries': ['미국', '캐나다'],
            'lat': 45.0, 'lon': -100.0, 'weight': 1.4
        },
        '남미': {
            'countries': ['브라질', '아르헨티나', '칠레'],
            'lat': -15.0, 'lon': -60.0, 'weight': 0.8
        },
        '아프리카': {
            'countries': ['남아프리카공화국', '이집트', '모로코'],
            'lat': 0.0, 'lon': 20.0, 'weight': 0.6
        },
        '오세아니아': {
            'countries': ['호주', '뉴질랜드'],
            'lat': -25.0, 'lon': 140.0, 'weight': 0.7
        }
    }
    
    # 기후기술 분야 및 세부 기술
    tech_data = {
        '감축': ['태양광', '풍력', '전기차', '배터리', '수소', 'ESS'],
        '적응': ['스마트팜', '물관리', '기후예측', '방재시스템'],
        '융복합': ['스마트그리드', 'AI기후', '그린빌딩', '스마트시티']
    }
    
    data = []
    years = [2019, 2020, 2021, 2022]
    
    for year in years:
        for region, region_info in regions_info.items():
            for field, techs in tech_data.items():
                for tech in techs:
                    # 지역별 가중치와 기술별 인기도 반영
                    popular_techs = ['태양광', '전기차', '스마트그리드', '배터리']
                    tech_weight = 1.5 if tech in popular_techs else 1.0
                    
                    # 기본 진출 건수 (지역별, 기술별 차이)
                    base_count = np.random.randint(5, 50)
                    final_count = int(base_count * region_info['weight'] * tech_weight)
                    
                    # 연도별 증가 트렌드
                    year_multiplier = 1 + (year - 2019) * 0.15
                    final_count = int(final_count * year_multiplier)
                    
                    data.append({
                        'year': year,
                        'region': region,
                        'field': field,
                        'tech_name': tech,
                        'export_count': final_count,
                        'latitude': region_info['lat'],
                        'longitude': region_info['lon'],
                        'countries': ', '.join(region_info['countries'])
                    })
    
    return pd.DataFrame(data)

def filter_overseas_data(df, year, field):
    """해외진출 데이터 필터링"""
    filtered_df = df[df['year'] == year].copy()
    
    if field != "전체":
        filtered_df = filtered_df[filtered_df['field'] == field]
    
    return filtered_df

def create_arc_points(lat1, lon1, lat2, lon2, num_points=50):
    """두 점 사이의 아크(곡선) 포인트들을 생성"""
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # 두 점 사이의 거리 계산
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    # 간단한 아크 포인트 생성
    points = []
    for i in range(num_points + 1):
        f = i / num_points
        
        # 직선 보간
        lat = lat1 + f * dlat
        lon = lon1 + f * dlon
        
        # 아크 효과를 위한 높이 조정
        height_factor = math.sin(math.pi * f) * 0.3
        lat += height_factor * max(abs(dlat), abs(dlon)) * 0.2
        
        points.append((lat, lon))
    
    return points

def create_arc_flow_map(data):
    """한국에서 각 지역으로 아크형 플로우를 그리는 인터랙티브 지도"""
    if data.empty:
        return go.Figure().add_annotation(text="데이터가 없습니다", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # 한국 좌표
    korea_lat, korea_lon = 37.5665, 126.9780
    
    # 지역별 진출 건수 집계
    region_summary = data.groupby(['region', 'latitude', 'longitude']).agg({
        'export_count': 'sum',
        'tech_name': 'count',
        'countries': 'first'
    }).reset_index()
    
    # Plotly 지도 생성
    fig = go.Figure()
    
    # 한국 마커 추가 (별 모양으로 강조)
    fig.add_trace(go.Scattergeo(
        lon=[korea_lon],
        lat=[korea_lat],
        mode='markers+text',
        marker=dict(
            size=25,
            color='red',
            symbol='star',
            line=dict(width=3, color='white')
        ),
        text=['🇰🇷 한국'],
        textposition='top center',
        name='한국',
        hovertemplate='<b>한국</b><br>기후기술 수출 본부<extra></extra>'
    ))
    
    # 색상 팔레트 (진출 건수에 따라)
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6', '#e67e22']
    max_exports = region_summary['export_count'].max()
    
    # 각 지역에 대한 아크 라인과 마커 추가
    for i, row in region_summary.iterrows():
        # 아크 라인을 위한 중간점들 계산
        arc_points = create_arc_points(korea_lat, korea_lon, row['latitude'], row['longitude'])
        
        # 진출 건수에 따른 색상과 굵기 결정
        normalized_value = row['export_count'] / max_exports
        line_width = 2 + normalized_value * 6  # 2-8px
        color_idx = min(int(normalized_value * len(colors)), len(colors) - 1)
        line_color = colors[color_idx]
        
        # 아크 라인 추가
        fig.add_trace(go.Scattergeo(
            lon=[p[1] for p in arc_points],
            lat=[p[0] for p in arc_points],
            mode='lines',
            line=dict(
                width=line_width, 
                color=line_color,
            ),
            opacity=0.8,
            showlegend=False,
            hoverinfo='skip',
            name=f'Flow to {row["region"]}'
        ))
        
        # 목적지 마커 추가 (크기는 진출 건수에 비례)
        marker_size = 12 + normalized_value * 20  # 12-32px
        
        fig.add_trace(go.Scattergeo(
            lon=[row['longitude']],
            lat=[row['latitude']],
            mode='markers+text',
            marker=dict(
                size=marker_size,
                color=line_color,
                opacity=0.9,
                line=dict(width=2, color='white'),
                symbol='circle'
            ),
            text=[row['region']],
            textposition='top center',
            textfont=dict(size=10, color='black'),
            name=row['region'],
            hovertemplate=f'<b>{row["region"]}</b><br>' +
                         f'📊 진출 건수: {row["export_count"]:,}<br>' +
                         f'🔧 기술 수: {row["tech_name"]}<br>' +
                         f'🌍 주요 국가: {row["countries"]}<extra></extra>'
        ))
    
    # 레이아웃 설정
    fig.update_layout(
        title={
            'text': '🌏 한국 기후기술 해외진출 아크 플로우 맵',
            'x': 0.5,
            'font': {'size': 18, 'color': '#2c3e50', 'family': 'Arial Black'}
        },
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(240, 240, 240)',
            coastlinecolor='rgb(180, 180, 180)',
            showocean=True,
            oceancolor='rgb(230, 245, 255)',
            showlakes=True,
            lakecolor='rgb(230, 245, 255)',
            showrivers=True,
            rivercolor='rgb(230, 245, 255)',
            bgcolor='rgba(0,0,0,0)',
            showframe=False,
            showcoastlines=True,
            projection_scale=1
        ),
        height=600,
        showlegend=False,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def create_animated_flow_map(data):
    """애니메이션 효과가 있는 플로우 지도"""
    if data.empty:
        return go.Figure()
    
    # 한국 좌표
    korea_lat, korea_lon = 37.5665, 126.9780
    
    # 지역별 데이터 준비
    region_summary = data.groupby(['region', 'latitude', 'longitude']).agg({
        'export_count': 'sum',
        'tech_name': 'count',
        'countries': 'first'
    }).reset_index()
    
    # 애니메이션 프레임 생성
    frames = []
    
    for frame_num in range(20):  # 20프레임
        frame_data = []
        
        # 한국 마커 (항상 표시)
        frame_data.append(go.Scattergeo(
            lon=[korea_lon],
            lat=[korea_lat],
            mode='markers+text',
            marker=dict(size=25, color='red', symbol='star', line=dict(width=3, color='white')),
            text=['🇰🇷 한국'],
            textposition='top center',
            name='한국'
        ))
        
        # 각 지역에 대해 점진적으로 라인 표시
        for i, row in region_summary.iterrows():
            if frame_num >= i * 2:  # 지연 효과
                arc_points = create_arc_points(korea_lat, korea_lon, row['latitude'], row['longitude'])
                
                # 현재 프레임에서 표시할 점들의 수
                visible_points = min(len(arc_points), 
                                   max(1, int(len(arc_points) * (frame_num - i * 2) / 10)))
                
                current_points = arc_points[:visible_points]
                
                # 아크 라인
                frame_data.append(go.Scattergeo(
                    lon=[p[1] for p in current_points],
                    lat=[p[0] for p in current_points],
                    mode='lines',
                    line=dict(width=4, color='#3498db'),
                    opacity=0.8,
                    showlegend=False
                ))
                
                # 목적지 마커 (라인이 완성되면 표시)
                if visible_points >= len(arc_points):
                    frame_data.append(go.Scattergeo(
                        lon=[row['longitude']],
                        lat=[row['latitude']],
                        mode='markers+text',
                        marker=dict(size=15, color='#2ecc71', line=dict(width=2, color='white')),
                        text=[row['region']],
                        textposition='top center',
                        name=row['region']
                    ))
        
        frames.append(go.Frame(data=frame_data, name=str(frame_num)))
    
    # 초기 프레임
    fig = go.Figure(data=frames[0].data, frames=frames)
    
    # 애니메이션 버튼 추가
    fig.update_layout(
        title='🌏 애니메이션 플로우 맵',
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(240, 240, 240)',
            oceancolor='rgb(230, 245, 255)',
        ),
        height=600,
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'y': 0.9,
            'x': 0.1,
            'buttons': [
                {
                    'label': '▶️ 재생',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 300, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 200}
                    }]
                },
                {
                    'label': '⏸️ 정지',
                    'method': 'animate',
                    'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                }
            ]
        }]
    )
    
    return fig

def create_3d_globe_flow(data):
    """3D 지구본 스타일 플로우 맵"""
    if data.empty:
        return go.Figure()
    
    # 한국 좌표
    korea_lat, korea_lon = 37.5665, 126.9780
    
    # 지역별 데이터
    region_summary = data.groupby(['region', 'latitude', 'longitude']).agg({
        'export_count': 'sum',
        'tech_name': 'count',
        'countries': 'first'
    }).reset_index()
    
    fig = go.Figure()
    
    # 한국 마커 추가
    fig.add_trace(go.Scatter3d(
        x=[korea_lon],
        y=[korea_lat],
        z=[0],
        mode='markers+text',
        marker=dict(size=15, color='red', symbol='diamond'),
        text=['🇰🇷 한국'],
        textposition='top center',
        name='한국'
    ))
    
    # 3D 아크 라인들
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
    
    for i, row in region_summary.iterrows():
        # 아크 포인트 생성
        arc_points = create_arc_points(korea_lat, korea_lon, row['latitude'], row['longitude'])
        
        # 높이 정보 추가 (Z축)
        heights = [math.sin(math.pi * j / len(arc_points)) * 50 for j in range(len(arc_points))]
        
        color_idx = i % len(colors)
        
        # 3D 라인 추가
        fig.add_trace(go.Scatter3d(
            x=[p[1] for p in arc_points],
            y=[p[0] for p in arc_points],
            z=heights,
            mode='lines',
            line=dict(width=6, color=colors[color_idx]),
            name=row['region'],
            hovertemplate=f'<b>{row["region"]}</b><br>진출 건수: {row["export_count"]:,}<extra></extra>'
        ))
        
        # 목적지 마커
        fig.add_trace(go.Scatter3d(
            x=[row['longitude']],
            y=[row['latitude']],
            z=[0],
            mode='markers+text',
            marker=dict(size=10, color=colors[color_idx]),
            text=[row['region']],
            textposition='top center',
            showlegend=False
        ))
    
    # 3D 레이아웃
    fig.update_layout(
        title='🌍 3D 지구본 플로우 맵',
        scene=dict(
            xaxis_title='경도',
            yaxis_title='위도',
            zaxis_title='높이',
            bgcolor='rgba(0,0,0,0.1)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        height=700
    )
    
    return fig

def get_top7_data(data):
    """해외진출 Top 7 데이터"""
    if data.empty:
        return pd.DataFrame()
    
    top7 = data.groupby(['region', 'tech_name']).agg({
        'export_count': 'sum'
    }).reset_index()
    
    top7 = top7.sort_values('export_count', ascending=False).head(7)
    top7['rank'] = range(1, len(top7) + 1)
    
    return top7

def create_region_chart(data, selected_region=None):
    """지역별 진출 현황 차트"""
    if data.empty:
        return go.Figure().add_annotation(text="데이터가 없습니다", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # 지역별 집계
    region_data = data.groupby(['region', 'field'])['export_count'].sum().reset_index()
    
    fig = px.bar(
        region_data,
        x='region',
        y='export_count',
        color='field',
        title="지역별 기후기술 진출 현황",
        labels={'export_count': '진출 건수', 'region': '지역'},
        color_discrete_map={
            '감축': '#1f77b4',
            '적응': '#ff7f0e',
            '융복합': '#2ca02c'
        }
    )
    
    # 선택된 지역 하이라이트
    if selected_region:
        fig.update_traces(
            opacity=0.3
        )
        # 선택된 지역만 불투명하게
        for trace in fig.data:
            if selected_region in trace.name:
                trace.opacity = 1.0
    
    fig.update_layout(
        height=400,
        title_x=0.5,
        xaxis_title="지역",
        yaxis_title="진출 건수",
        xaxis={'categoryorder': 'total descending'}
    )
    
    return fig

def create_tech_chart(data, selected_tech=None):
    """기술별 진출 현황 차트"""
    if data.empty:
        return go.Figure().add_annotation(text="데이터가 없습니다", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    tech_data = data.groupby(['tech_name', 'field'])['export_count'].sum().reset_index()
    tech_data = tech_data.sort_values('export_count', ascending=True)
    
    fig = px.bar(
        tech_data,
        x='export_count',
        y='tech_name',
        color='field',
        orientation='h',
        title="기술별 해외진출 현황",
        labels={'export_count': '진출 건수', 'tech_name': '기술명'},
        color_discrete_map={
            '감축': '#1f77b4',
            '적응': '#ff7f0e',
            '융복합': '#2ca02c'
        }
    )
    
    # 선택된 기술 하이라이트
    if selected_tech:
        fig.update_traces(opacity=0.3)
        for trace in fig.data:
            if selected_tech in trace.name:
                trace.opacity = 1.0
    
    fig.update_layout(
        height=500,
        title_x=0.5,
        xaxis_title="진출 건수",
        yaxis_title="기술명"
    )
    
    return fig

def create_flow_diagram(data):
    """진출 흐름도 (Sankey diagram)"""
    if data.empty:
        return go.Figure().add_annotation(text="데이터가 없습니다", 
                                        xref="paper", yref="paper", 
                                        x=0.5, y=0.5, showarrow=False)
    
    # 한국 -> 지역 -> 기술 흐름 데이터 준비
    flows = data.groupby(['field', 'region', 'tech_name'])['export_count'].sum().reset_index()
    flows = flows.sort_values('export_count', ascending=False).head(20)  # 상위 20개만
    
    # 노드 레이블 생성
    fields = flows['field'].unique()
    regions = flows['region'].unique()
    techs = flows['tech_name'].unique()
    
    all_labels = ['한국'] + list(fields) + list(regions) + list(techs)
    
    # 노드 인덱스 매핑
    label_to_idx = {label: i for i, label in enumerate(all_labels)}
    
    # 링크 데이터 생성
    source = []
    target = []
    value = []
    
    # 한국 -> 분야
    for field in fields:
        field_total = flows[flows['field'] == field]['export_count'].sum()
        source.append(label_to_idx['한국'])
        target.append(label_to_idx[field])
        value.append(field_total)
    
    # 분야 -> 지역
    for _, row in flows.iterrows():
        source.append(label_to_idx[row['field']])
        target.append(label_to_idx[row['region']])
        value.append(row['export_count'])
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_labels,
            color="rgba(78, 205, 196, 0.8)"
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color="rgba(78, 205, 196, 0.4)"
        )
    )])
    
    fig.update_layout(
        title_text="기후기술 해외진출 흐름도",
        title_x=0.5,
        height=400,
        font_size=12
    )
    
    return fig

def main():
    st.title("🌏 기후기술 해외진출 현황")
    
    # 데이터 로드
    overseas_data = load_overseas_data()
    
    # 사이드바 컨트롤
    st.sidebar.header("🔧 필터 설정")
    
    # 연도 선택
    years = sorted(overseas_data['year'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("연도", years)
    
    # 기술분야 선택
    fields = ["전체"] + sorted(overseas_data['field'].unique().tolist())
    selected_field = st.sidebar.selectbox("기후기술 분야", fields)
    
    # 데이터 필터링
    filtered_data = filter_overseas_data(overseas_data, selected_year, selected_field)
    
    # 요약 통계
    st.subheader(f"📊 {selected_year}년 해외진출 현황")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_exports = filtered_data['export_count'].sum()
        st.markdown(f"""
        <div class="overseas-card">
            <h3>{total_exports:,}</h3>
            <p>총 진출 건수</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        unique_regions = filtered_data['region'].nunique()
        st.markdown(f"""
        <div class="overseas-card">
            <h3>{unique_regions}</h3>
            <p>진출 지역 수</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        unique_techs = filtered_data['tech_name'].nunique()
        st.markdown(f"""
        <div class="overseas-card">
            <h3>{unique_techs}</h3>
            <p>진출 기술 수</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # 최다 진출 지역
        if not filtered_data.empty:
            top_region = filtered_data.groupby('region')['export_count'].sum().idxmax()
        else:
            top_region = "없음"
        
        st.markdown(f"""
        <div class="overseas-card">
            <h3>{top_region}</h3>
            <p>최다 진출 지역</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 세계지도 섹션
    st.subheader("🗺️ 세계 진출 현황")
    
    # 지도 타입 선택 옵션 추가
    col1, col2 = st.columns([3, 1])
    
    with col2:
        map_type = st.selectbox(
            "지도 타입",
            options=["아크형 플로우", "애니메이션", "3D 지구본"],
            index=0
        )
    
    with col1:
        st.write("") # 빈 공간
    
    # 지도 생성
    if map_type == "아크형 플로우":
        world_map = create_arc_flow_map(filtered_data)
        st.plotly_chart(world_map, use_container_width=True)
    elif map_type == "애니메이션":
        world_map = create_animated_flow_map(filtered_data)
        st.plotly_chart(world_map, use_container_width=True)
    elif map_type == "3D 지구본":
        world_map = create_3d_globe_flow(filtered_data)
        st.plotly_chart(world_map, use_container_width=True)
    
    # 지도 설명 추가
    st.info("💡 **지도 사용법:** 마커를 클릭하면 상세 정보를 볼 수 있습니다. 선의 굵기와 색상은 진출 건수를 나타냅니다.")
    
    # 메인 분석 섹션
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 진출 흐름도
        st.subheader("🌊 진출 흐름도")
        flow_fig = create_flow_diagram(filtered_data)
        st.plotly_chart(flow_fig, use_container_width=True)
    
    with col2:
        # 해외진출 Top 7
        st.subheader("🏆 해외진출 Top 7")
        top7_data = get_top7_data(filtered_data)
        
        if not top7_data.empty:
            for _, row in top7_data.iterrows():
                st.markdown(f"""
                <div class="top7-item">
                    <strong>{row['rank']}. {row['region']} - {row['tech_name']}</strong><br>
                    <span style="color: #4ecdc4; font-weight: bold;">{row['export_count']:,}건</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("표시할 데이터가 없습니다.")
    
    # 지역별 및 기술별 차트
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌍 지역별 진출 현황")
        region_fig = create_region_chart(filtered_data)
        st.plotly_chart(region_fig, use_container_width=True)
    
    with col2:
        st.subheader("🔬 기술별 진출 현황")
        tech_fig = create_tech_chart(filtered_data)
        st.plotly_chart(tech_fig, use_container_width=True)
    
    # 기술 종류별 색상 범례
    st.subheader("🎨 기술 분야 범례")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="region-card" style="border-left-color: #1f77b4;">
            <strong>🔋 감축 기술</strong><br>
            <small>온실가스 감축을 위한 기술</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="region-card" style="border-left-color: #ff7f0e;">
            <strong>🛡️ 적응 기술</strong><br>
            <small>기후변화 적응을 위한 기술</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="region-card" style="border-left-color: #2ca02c;">
            <strong>🔗 융복합 기술</strong><br>
            <small>ICT와 융합된 기술</small>
        </div>
        """, unsafe_allow_html=True)
    
    # 연도별 트렌드 분석
    if len(overseas_data['year'].unique()) > 1:
        st.subheader("📈 연도별 진출 트렌드")
        
        # 연도별 진출 현황
        yearly_trend = overseas_data.groupby(['year', 'field'])['export_count'].sum().reset_index()
        
        trend_fig = px.line(
            yearly_trend,
            x='year',
            y='export_count',
            color='field',
            title="연도별 분야별 해외진출 트렌드",
            labels={'year': '연도', 'export_count': '진출 건수'},
            markers=True,
            color_discrete_map={
                '감축': '#1f77b4',
                '적응': '#ff7f0e',
                '융복합': '#2ca02c'
            }
        )
        
        trend_fig.update_layout(
            height=400,
            title_x=0.5,
            xaxis_title="연도",
            yaxis_title="진출 건수"
        )
        
        trend_fig.update_traces(
            line=dict(width=3),
            marker=dict(size=8)
        )
        
        st.plotly_chart(trend_fig, use_container_width=True)
        
        # 성장률 분석
        st.subheader("📊 성장률 분석")
        
        # 최근 2년간 성장률 계산
        recent_years = sorted(overseas_data['year'].unique())[-2:]
        if len(recent_years) >= 2:
            older_year, newer_year = recent_years[0], recent_years[1]
            
            older_data = overseas_data[overseas_data['year'] == older_year]['export_count'].sum()
            newer_data = overseas_data[overseas_data['year'] == newer_year]['export_count'].sum()
            
            if older_data > 0:
                growth_rate = ((newer_data - older_data) / older_data) * 100
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(f"{older_year}년 진출", f"{older_data:,}건")
                
                with col2:
                    st.metric(f"{newer_year}년 진출", f"{newer_data:,}건")
                
                with col3:
                    st.metric("성장률", f"{growth_rate:+.1f}%")
    
    # 상세 분석 섹션
    if st.checkbox("📋 상세 분석 보기"):
        st.subheader("📄 상세 데이터")
        
        # 상세 데이터 표시
        detail_data = filtered_data.groupby(['region', 'tech_name', 'field']).agg({
            'export_count': 'sum',
            'countries': 'first'
        }).reset_index()
        
        # 정렬
        sort_by = st.selectbox("정렬 기준", ['진출건수', '지역', '기술명'])
        ascending = st.radio("정렬 순서", ["내림차순", "오름차순"]) == "오름차순"
        
        sort_columns = {
            '진출건수': 'export_count',
            '지역': 'region',
            '기술명': 'tech_name'
        }
        
        sorted_data = detail_data.sort_values(
            sort_columns[sort_by],
            ascending=ascending
        )
        
        # 컬럼명 한글화
        display_data = sorted_data.copy()
        display_data.columns = ['지역', '기술명', '분야', '진출건수', '주요국가']
        
        st.dataframe(display_data, use_container_width=True)
        
        # 요약 통계
        st.subheader("📊 요약 통계")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("총 진출 건수", f"{detail_data['export_count'].sum():,}")
            st.metric("평균 진출 건수", f"{detail_data['export_count'].mean():.1f}")
        
        with col2:
            st.metric("최대 진출 건수", f"{detail_data['export_count'].max():,}")
            st.metric("최소 진출 건수", f"{detail_data['export_count'].min():,}")
        
        with col3:
            st.metric("진출 지역 수", f"{detail_data['region'].nunique()}")
            st.metric("진출 기술 수", f"{detail_data['tech_name'].nunique()}")
        
        # 지역별 상세 분석
        st.subheader("🌍 지역별 상세 분석")
        
        region_analysis = detail_data.groupby('region').agg({
            'export_count': ['sum', 'mean', 'count'],
            'tech_name': 'nunique'
        }).round(1)
        
        region_analysis.columns = ['총진출건수', '평균진출건수', '진출기술수', '기술종류수']
        region_analysis = region_analysis.reset_index()
        region_analysis.columns = ['지역', '총진출건수', '평균진출건수', '진출기술수', '기술종류수']
        
        st.dataframe(region_analysis, use_container_width=True)
        
        # 데이터 다운로드
        csv = display_data.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 CSV 다운로드",
            data=csv,
            file_name=f"해외진출_{selected_year}년_{selected_field}.csv",
            mime="text/csv"
        )
    
    # 추가 인사이트 섹션
    st.subheader("💡 주요 인사이트")
    
    if not filtered_data.empty:
        # 인사이트 계산
        top_region = filtered_data.groupby('region')['export_count'].sum().idxmax()
        top_tech = filtered_data.groupby('tech_name')['export_count'].sum().idxmax()
        top_field = filtered_data.groupby('field')['export_count'].sum().idxmax()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="region-card">
                <strong>🎯 핵심 진출 지역</strong><br>
                <span style="color: #4ecdc4; font-size: 18px; font-weight: bold;">{top_region}</span><br>
                <small>가장 많은 기술 진출이 이루어진 지역</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="region-card">
                <strong>🔬 주력 기술</strong><br>
                <span style="color: #4ecdc4; font-size: 18px; font-weight: bold;">{top_tech}</span><br>
                <small>해외 진출에서 가장 높은 성과를 보인 기술</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="region-card">
                <strong>🏆 우세 분야</strong><br>
                <span style="color: #4ecdc4; font-size: 18px; font-weight: bold;">{top_field}</span><br>
                <small>가장 활발한 해외 진출을 보인 기술 분야</small>
            </div>
            """, unsafe_allow_html=True)
            
            # 지역 다양성 지수 계산
            region_diversity = filtered_data['region'].nunique()
            total_regions = 9  # 전체 지역 수
            diversity_score = (region_diversity / total_regions) * 100
            
            st.markdown(f"""
            <div class="region-card">
                <strong>🌐 지역 다양성</strong><br>
                <span style="color: #4ecdc4; font-size: 18px; font-weight: bold;">{diversity_score:.1f}%</span><br>
                <small>전체 지역 중 진출한 지역 비율</small>
            </div>
            """, unsafe_allow_html=True)
    
    # 홈으로 돌아가기
    if st.button("🏠 메인으로 돌아가기"):
        st.switch_page("main.py")

if __name__ == "__main__":
    main()
