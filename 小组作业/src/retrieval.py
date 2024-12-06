import heapq
import json
from itertools import combinations
from utils import setup_logger, load_config
from PageRank import build_co_occurrence_graph


# 位置权重：根据字的位置赋予不同的权重
def position_weight(index, total_length):
    if index == 0 or index == total_length - 1:
        return 1.2  # 开头和结尾位置权重较高
    else:
        return 1.0  # 中间位置权重较低


# 计算排列的评分（包括PageRank分数和位置权重）
def calculate_weighted_score(permutation, pagerank_scores):
    total_score = 0
    total_length = len(permutation)
    for i, char in enumerate(permutation):
        score = pagerank_scores.get(char, 0)
        weight = position_weight(i, total_length)
        total_score += score * weight
    return total_score


# A* 搜索：通过启发式函数优化排列组合
def a_star_search(input_chars, target_length, pagerank_scores, poem_database):
    possible_combinations = list(combinations(input_chars, target_length))
    heap = []
    for comb in possible_combinations:
        score = calculate_weighted_score(comb, pagerank_scores)
        heapq.heappush(heap, (-score, comb))  # 采用负分值，以便最大值优先
    
    while heap:
        best_score, best_comb = heapq.heappop(heap)
        best_poem = "".join(best_comb)
        if best_poem in poem_database:
            return best_poem, -best_score
    
    return None, None


from itertools import permutations
from tqdm import tqdm  # 用于显示进度条

def brute_force_search_with_progress(input_chars, target_length, pagerank_scores, poem_database):
    best_poem = None
    best_score = float('-inf')

    # 统计所有可能的排列数量
    total_combinations = sum(len(list(permutations(input_chars, length))) for length in range(1, target_length + 1))

    # 使用 tqdm 显示进度条
    with tqdm(total=total_combinations, desc="搜索进度") as pbar:
        for length in range(1, target_length + 1):  # 支持不同长度
            for perm in permutations(input_chars, length):
                candidate = "".join(perm)
                score = calculate_weighted_score(perm, pagerank_scores)

                # 检查数据库中是否有该诗句
                if candidate in poem_database:
                    if score > best_score:
                        best_poem = candidate
                        best_score = score

                pbar.update(1)  # 更新进度条

    return best_poem, best_score



# 主程序：进行诗句检索
def main():
    config = load_config()
    log_dir = config["log_directory"]
    logger = setup_logger(log_dir)
    
    input_chars = ["明", "月", "光", "松", "間", "照", "清", "泉", "石"]
    target_length = config["retrieval_target_length"]

    logger.info("开始加载数据库...")
    with open(config["processed_poem_file"], "r", encoding="utf-8") as f:
        database = json.load(f)

    poem_database = database["poem_database"]
    pagerank_scores = database["pagerank_scores"]
    
    # 打印数据库内容和PageRank分数
    logger.debug(f"诗句数据库: {poem_database}")
    logger.debug(f"PageRank分数: {pagerank_scores}")
    
    logger.info("数据库加载完成，开始检索...")

    # 调用暴力搜索（带进度条）
    best_poem, best_score = brute_force_search_with_progress(input_chars, target_length, pagerank_scores, poem_database)

    if best_poem:
        logger.info(f"找到诗句：{best_poem}，评分：{best_score}")
    else:
        logger.warning("未找到符合条件的诗句！")

if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()