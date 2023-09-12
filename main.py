import statistics
import matplotlib.pyplot as plt
import pandas as pd

# Global variables
final_scores = {}


# Calculates the score of each player based on a certain metric
def get_score(df_dict, max_points, amount):
    res = {}
    # The difference in points between each placing
    margin = max_points / amount
    # Assign each player with a score depending on their rank
    for player, rank in df_dict.items():
        res[player] = max_points - (rank * margin)
    return res


def print_score(_dict, stat):
    print(f"{stat} Scores:")
    for player, score in _dict.items():
        print(f"{player}: {score}")
    print("\n")


def get_best_scorers():
    global final_scores
    df_ppg = pd.read_csv('data/PPG.csv')
    df_pts = pd.read_csv('data/PTS.csv')
    df_tsp = pd.read_csv('data/TSP.csv')
    df_ows = pd.read_csv('data/OWS.csv')

    # Subtract one from the ranks to better fit the calculations
    df_ppg['Rank'] = df_ppg['Rank'] - 1
    df_pts['Rank'] = df_pts['Rank'] - 1
    df_tsp['Rank'] = df_tsp['Rank'] - 1
    df_ows['Rank'] = df_ows['Rank'] - 1

    # Sort dataframe in ascending order and select the top 20 players
    top_20_ppg = df_ppg.nsmallest(20, 'Rank')
    top_20_pts = df_pts.nsmallest(20, 'Rank')
    top_20_tsp = df_tsp.nsmallest(20, 'Rank')
    top_20_ows = df_ows.nsmallest(20, 'Rank')

    ppg_rank_dict = dict(zip(top_20_ppg['Player'], top_20_ppg['Rank']))
    pts_rank_dict = dict(zip(top_20_pts['Player'], top_20_pts['Rank']))
    tsp_rank_dict = dict(zip(top_20_tsp['Player'], top_20_tsp['Rank']))
    ows_rank_dict = dict(zip(top_20_ows['Player'], top_20_ows['Rank']))

    # Dictionaries of all the scores for each metric
    ppg_scores = get_score(ppg_rank_dict, 40, 20)
    pts_scores = get_score(pts_rank_dict, 25, 20)
    tsp_scores = get_score(tsp_rank_dict, 25, 20)
    ows_scores = get_score(ows_rank_dict, 10, 20)

    # Print scores for each individual stat
    print_score(ppg_scores, "PPG")
    print_score(pts_scores, "PTS")
    print_score(tsp_scores, "TSP")
    print_score(ows_scores, "OWS")

    all_dicts = [ppg_scores, pts_scores, tsp_scores, ows_scores]

    for d in all_dicts:
        for player, score in d.items():
            final_scores[player] = final_scores.get(player, 0) + score

    # Sort the final scores and find the player with the largest score and their score
    sorted_scores = dict(sorted(final_scores.items(), key=lambda item: item[1], reverse=True))
    player_with_largest_score = max(final_scores, key=final_scores.get)
    largest_score = final_scores[player_with_largest_score]

    # Print results
    print_score(sorted_scores, "Final")
    print(f"Player with largest score: {player_with_largest_score}, Score: {largest_score}\n")
    print("Number of players in the list:", len(sorted_scores))

    # Put data into csv
    save_dict_to_csv(sorted_scores, 'data/scoring_scores.csv', 'Player', 'Score')


def get_heights():
    global final_scores
    # Read the CSV file into a dataframe
    player_data = pd.read_csv('data/Player_data.csv')

    # Create a dictionary mapping player names to heights
    player_heights = dict(zip(player_data['Player'], player_data['height']))

    # Retrieve the heights of the top scorers using the player_heights dictionary
    top_scorer_heights = {player: player_heights.get(player, "Height Not Found") for player in final_scores}

    # Calculate summary statistics
    heights = [height for height in top_scorer_heights.values() if isinstance(height, (int, float))]
    mean_height = round(sum(heights) / len(heights), 2)
    median_height = round(statistics.median(heights), 2)
    mode_height = round(statistics.mode(heights), 2)

    # Print the heights and statistics
    for player, height in top_scorer_heights.items():
        print(f"{player}: {height} cm")

    # Print statistical summary
    print(f"Mean Height: {mean_height} cm")
    print(f"Median Height: {median_height} cm")
    print(f"Mode Height: {mode_height} cm\n")

    # Optional Data Visualization (Histogram)
    plt.hist(heights, bins=15, color='skyblue', edgecolor='black')
    plt.title("Height Distribution of Top Scorers")
    plt.xlabel("Height (cm)")
    plt.ylabel("Frequency")
    plt.show()

    # Finding optimal height
    height_scores = {}
    i = 0
    for height in top_scorer_heights.values():
        height_scores[height] = height_scores.get(height, 0) + 100 - i
        i += 1

    # Sort the height scores and find the optimal height
    sorted_height_scores = dict(sorted(height_scores.items(), key=lambda item: item[1], reverse=True))
    sorted_height_scores_by_height = dict(sorted(height_scores.items(), key=lambda item: item[0], reverse=False))
    optimal_height, best_height_score = list(sorted_height_scores.items())[0]
    print_score(sorted_height_scores, "Height")
    print(f"Optimal height: {optimal_height} cm")

    # Find all player who are of the optimal height
    print(f"Players who are {optimal_height} cm:")
    for player, height in top_scorer_heights.items():
        if height == optimal_height:
            print(player)

    # Save heights data into a csv named "heights.csv"
    save_dict_to_csv(sorted_height_scores_by_height, 'data/height_scores.csv', 'Height (cm)', 'Score')


def save_dict_to_csv(heights, filename, col1, col2):
    df = pd.DataFrame(list(heights.items()), columns=[col1, col2])
    df.to_csv(filename, index=False)


def main():
    get_best_scorers()
    get_heights()


if __name__ == '__main__':
    main()
