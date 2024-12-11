import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import os
os.environ["LOKY_MAX_CPU_COUNT"] = "4" 


# 파일 로드
correlation_matrix = pd.read_csv("data\menu_correlation_matrix.csv", index_col=0)

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
cluster_labels = {
    0: "클러스터 1: 매운 음식",
    1: "클러스터 2: 고기 요리",
    2: "클러스터 3: 해산물 요리",
    3: "클러스터 4: 면 요리",
    4: "클러스터 5: 기타"
}

# 3. Plotly 산점도 생성
fig = go.Figure()

# 메뉴 간 연결선을 그리기 위해 모든 상관관계 확인
threshold = 0.4  # 낮은 임계값 설정
for i, menu_i in enumerate(correlation_matrix.index):
    for j, menu_j in enumerate(correlation_matrix.columns):
        if i < j and correlation_matrix.iloc[i, j] > threshold:
            fig.add_trace(
                go.Scatter(
                    x=[df_coordinates.loc[menu_i, "x"], df_coordinates.loc[menu_j, "x"]],
                    y=[df_coordinates.loc[menu_i, "y"], df_coordinates.loc[menu_j, "y"]],
                    mode="lines",
                    line=dict(width=0.5, color="lightgray", dash="solid"),  # 선의 투명도 제거
                    opacity=0.3,  # Scatter 전체에 투명도 적용
                    hoverinfo="none",
                )
            )

# 메뉴 점 추가 (모든 텍스트 표시 및 색상 적용)
fig.add_trace(
    go.Scatter(
        x=df_coordinates["x"],
        y=df_coordinates["y"],
        mode="markers+text",
        text=df_coordinates.index,
        hovertext=[
            f"메뉴: {menu}<br>유사한 메뉴: {', '.join(correlation_matrix.loc[menu].sort_values(ascending=False)[1:4].index)}"
            for menu in df_coordinates.index
        ],
        marker=dict(
            size=10,
            color=[colors[cluster] for cluster in df_coordinates["cluster"]],
            opacity=0.8,
            line=dict(width=1, color="black"),
        ),
        textfont=dict(size=10),
        textposition="top center",
    )
)

# 색상 설명 추가
annotations = [
    dict(
        x=1.2,
        y=1.5 - 0.1 * i,
        text=f"<b>{color}:</b> {label}",
        showarrow=False,
        font=dict(size=12),
        xanchor="left"
    )
    for i, (color, label) in enumerate(zip(colors, cluster_labels.values()))
]

fig.update_layout(
    title="메뉴 간 상관관계 지도 (더 많은 연결 표시)",
    xaxis=dict(title="PCA 1", showgrid=False, zeroline=False),
    yaxis=dict(title="PCA 2", showgrid=False, zeroline=False),
    showlegend=False,
    hovermode="closest",
    annotations=annotations
)

# 5. 시각화 표시
fig.show()
