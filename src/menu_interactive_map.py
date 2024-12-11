import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import os

os.environ["LOKY_MAX_CPU_COUNT"] = "4"

def generate_menu_map(correlation_matrix_path, user_preferences=None):
    # 파일 로드
    correlation_matrix = pd.read_csv(correlation_matrix_path, index_col=0)

    # 1. 차원 축소 (PCA를 사용해 2D 좌표 생성)
    pca = PCA(n_components=2)
    coordinates = pca.fit_transform(correlation_matrix)

    # 2. 군집화
    kmeans = KMeans(n_clusters=5, random_state=0).fit(coordinates)
    clusters = kmeans.labels_

    # 좌표 데이터프레임 생성
    df_coordinates = pd.DataFrame(coordinates, columns=["x", "y"], index=correlation_matrix.index)
    df_coordinates["cluster"] = clusters

    # 군집 색상 매핑
    colors = ["red", "blue", "green", "purple", "orange"]

    # 3. Plotly 산점도 생성
    fig = go.Figure()

    # 메뉴 간 연결선을 그리기 위해 모든 상관관계 확인
    threshold = 0.5  # 낮은 임계값 설정
    for i, menu_i in enumerate(correlation_matrix.index):
        for j, menu_j in enumerate(correlation_matrix.columns):
            if i < j and correlation_matrix.iloc[i, j] > threshold:
                fig.add_trace(
                    go.Scatter(
                        x=[df_coordinates.loc[menu_i, "x"], df_coordinates.loc[menu_j, "x"]],
                        y=[df_coordinates.loc[menu_i, "y"], df_coordinates.loc[menu_j, "y"]],
                        mode="lines",
                        line=dict(width=0.5, color="lightgray", dash="solid"),
                        opacity=0.9,  # 연결선 투명도 증가
                        hoverinfo="none",
                    )
                )

    # 사용자 선호도를 반영한 점 스타일
    marker_sizes = [
        25 if user_preferences and menu in user_preferences and user_preferences[menu] == 4 else 12
        for menu in df_coordinates.index
    ]
    marker_opacity = [
        0.9 if user_preferences and menu in user_preferences and user_preferences[menu] == 4 else 0.5
        for menu in df_coordinates.index
    ]
    marker_color = [
        "limegreen" if user_preferences and menu in user_preferences and user_preferences[menu] == 4 else colors[cluster]
        for menu, cluster in zip(df_coordinates.index, df_coordinates["cluster"])
    ]
    marker_line_width = [
        3 if user_preferences and menu in user_preferences and user_preferences[menu] == 4 else 1
        for menu in df_coordinates.index
    ]

    # 메뉴 점 추가
    fig.add_trace(
        go.Scatter(
            x=df_coordinates["x"],
            y=df_coordinates["y"],
            mode="markers+text",
            text=df_coordinates.index,
            hovertext=[
                f"메뉴: {menu}<br>유사한 메뉴: {', '.join(correlation_matrix.loc[menu].sort_values(ascending=False)[1:4].index)}"
                + (f"<br><b>사용자 선호 메뉴</b>" if user_preferences and menu in user_preferences and user_preferences[menu] == 4 else "")
                for menu in df_coordinates.index
            ],
            marker=dict(
                size=marker_sizes,
                color=marker_color,
                opacity=marker_opacity,
                line=dict(width=marker_line_width, color="black"),
            ),
            textfont=dict(size=10),
            textposition="top center",
        )
    )

    # 레이아웃 설정
    fig.update_layout(
        title="MenuMate의 메뉴 간 상관관계 지도",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),  # X축 제목 및 눈금 제거
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),  # Y축 제목 및 눈금 제거
        showlegend=False,
        hovermode="closest",
    )

    return fig
