import random
import json
from urllib.parse import urlencode
from datetime import datetime, date, timedelta

def suggest_content(num_suggestions, suggestion_frequency, content_list):
    # create dictionary to hold each movie's suggestion score
    suggestion_scores = {}
    suggested_content = {713704: datetime.strptime('2023-04-26', '%Y-%m-%d').date()}

    # calculate suggestion score for each movie based on release date and popularity
    for movie in content_list:
        release_date_str = movie['release_date']
        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
        days_until_release = abs((release_date - date.today()).days)

        if (days_until_release == 0):
            suggestion_scores[movie['id']] = movie['popularity']
            continue

        suggestion_score = movie['popularity'] / days_until_release
        suggestion_scores[movie['id']] = suggestion_score


    # sort content by suggestion score in descending order
    sorted_content = sorted(content_list, key=lambda x: suggestion_scores[x['id']], reverse=True)

    # create list to hold final movie suggestions
    final_suggestions = []

    # add num_suggestions movies to final_suggestions, avoiding duplicates and previously suggested movies
    while len(final_suggestions) < num_suggestions and len(final_suggestions) < len(sorted_content):
        suggestion_added = False
        for movie in sorted_content:
            if len(final_suggestions) == num_suggestions:
                break

            # check if movie has already been suggested
            if movie['id'] in suggested_content:
                last_suggested_date = suggested_content[movie['id']]
                days_since_suggestion = (date.today() - last_suggested_date).days

                # calculate suggestion score for previously suggested movie based on how long ago it was suggested
                if days_since_suggestion == 0:
                    suggestion_score = 0
                elif days_since_suggestion > suggestion_frequency:
                    suggestion_score = suggestion_scores[movie['id']] / days_since_suggestion
                else:
                    suggestion_score = suggestion_scores[movie['id']] * 0.5

                # check if previously suggested movie's suggestion score is higher than the next movie's suggestion score
                if len(final_suggestions) > 0 and suggestion_score > suggestion_scores[final_suggestions[-1]['id']]:
                    final_suggestions.append(movie)
                    suggested_content[movie['id']] = date.today()
                    suggestion_added = True
                    break

            # check if movie has not been previously suggested
            else:
                final_suggestions.append(movie)
                suggested_content[movie['id']] = date.today()
                suggestion_added = True
                break

        # if no suggestions were added in the previous for loop, break out of the while loop
        if not suggestion_added:
            break

    # If there are not enough suggestions, add additional suggestions from the sorted content
    while len(final_suggestions) < num_suggestions and len(final_suggestions) < len(sorted_content):
        movie = sorted_content[len(final_suggestions)]
        if movie['id'] not in suggested_content:
            final_suggestions.append(movie)
            suggested_content[movie['id']] = date.today()

    print(json.dumps(final_suggestions))
    return final_suggestions