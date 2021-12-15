document.getElementById("search_tweets").addEventListener("click", display_search_tweets);
var dashboard = document.getElementById("dashboard").addEventListener("click", display_search_tweets_dashboard);
var list = null;

function display_search_tweets() {
    console.log("search");
    document.getElementById("search_tab").style.display = "block";
    document.getElementById("chart_tab").style.display = "none";
    document.getElementById("tweets-widget-container").style.display = "none";

}

function display_search_tweets_dashboard() {
    console.log("dashboard");
    document.getElementById("search_tab").style.display = "none";
    document.getElementById("chart_tab").style.display = "grid";
    document.getElementById("tweets-widget-container").style.display = "grid";
    get_query_list();

    // dasboard tab onload here ()
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
var form = document.getElementById("search_tab");
console.log(form);
form.addEventListener('submit', function(e) {
    e.preventDefault();
    console.log("Form submitted");
    var url = "http://127.0.0.1:8000/api/query-create/";

    var include_keywords = document.getElementById("Include keywords").value;
    var exclude_keywords = document.getElementById("Exclude keywords").value;
    var include_phrase = document.getElementById("Include phrase").value;
    var exclude_phrase = document.getElementById("Exclude phrase").value;
    var from_who = document.getElementById("from_who").value;
    var hashtags = document.getElementById("hashtags").value;
    var geo = document.getElementById("geo").checked;
    var language = document.getElementById("language").value;
    var query_name = document.getElementById("query_name").value;

    var lang = "lang: " + language;
    var query_string = include_keywords + " " + exclude_keywords + " " + include_phrase + " " + exclude_phrase + " " + from_who + " " + hashtags + " " + lang + " ";
    var date_created_at = new Date().toISOString().split("T")[0];
    try {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'query_string': query_string,
                'query_name': query_name,
                'geo': geo,
                'date_created_at': date_created_at
            })

        }).then(function(response) {
            document.getElementById('search_form').reset;
            window.alert('Searching');
        })
    } catch (error) {
        console.log(error);
    }
})

var checkbox = document.getElementById('checkdate');
checkbox.addEventListener('change', checkdate);
var date_picker = document.getElementById('date_created_at');

function checkdate() {
    if (this.checked) {
        console.log("checked");
        date_picker.disabled = true;
    } else {
        date_picker.disabled = false;

    }
}

function get_query_list() {
    var query_dropdown = document.getElementById("get_id");
    query_dropdown.innerHTML = "";

    var url = "http://127.0.0.1:8000/api/query-list/";
    fetch(url)
        .then((resp) => resp.json())
        .then(function(data) {
            console.log("DATA: ", data);
            list = data;
            for (var i in list) {
                var option = `<option value=\"${list[i].id}\">${list[i].id} - ${list[i].query_name}</option>`;
                query_dropdown.innerHTML += option;
            }
        })
}

var query_id = document.getElementById('get_id');
query_id.addEventListener("change", function(e) {
    e.preventDefault()
    id = query_id.value;
    // console.log(list);
    // console.log(id);
    for (var i = 0; i < list.length; i++) {
        //console.log(i);;
        // console.log(list[i]);
        //console.log(list[i].id);
        if (list[i].id == id) {
            var date_created = list[i].date_created_at;
            date_created = new Date(date_created);
            var a_week_ago = new Date(date_created.getTime() - (7 * 24 * 60 * 60 * 1000));

            var date_picker = document.getElementById("date_created_at");
            //console.log(a_week_ago.toISOString());
            //console.log(date_created.toISOString());
            var formatted_min_date = a_week_ago.toISOString().split('T')[0];
            var formatted_max_date = date_created.toISOString().split('T')[0];
            date_picker.setAttribute("min", formatted_min_date);
            date_picker.setAttribute("max", formatted_max_date);
            date_picker.setAttribute("value", formatted_max_date);
            document.getElementById('query_string').value = list[i].query_string;
            break;
        }
    }
})

var filter_form = document.getElementById("filter_form");

filter_form.addEventListener('submit', function(e) {
    e.preventDefault();
    var url = "http://127.0.0.1:8000/api/query-filter/";

    var query_id = document.getElementById("get_id").value;
    var checkdate = document.getElementById("checkdate").checked;
    var date_created_at = "All";
    if (checkdate == false) {
        var date_created_at = document.getElementById("date_created_at").value;
    }
    url += query_id + "/" + date_created_at;
    console.log(url);
    var word_frequency;
    var tweet_distribution;
    var time_series;
    const getData = async() => {
        const response = await fetch(url);
        const data = await response.json();
        console.log(data);
        word_frequency = data.Word_Frequency;
        tweet_distribution = data.Sentiment_Count;
        time_series = data.Time_Series;
        top_10_retweeted = data["Top_10_retweeted"]
        top_10_liked = data["Top_10_liked"]
        console.log(word_frequency);
        //console.log(typeof(word_frequency));

        console.log(tweet_distribution);
        //console.log(typeof(tweet_distribution));

        console.log(time_series);
        //console.log(typeof(time_series));

        /*console.log(word_frequency[0]);
        console.log(word_frequency[0].Words);
        console.log(word_frequency[0].Count);
        console.log(tweet_distribution[0].Sentiment);
        console.log(tweet_distribution[0]["Total Tweets"]);*/
        if (tweet_distribution != "")
            drawDonutChart(tweet_distribution);
        else {
            document.getElementById("TweetSentimentDonutChart").remove(); // remove canvas old chart
            document.getElementById("donut-chart").innerHTML = '<canvas id="TweetSentimentDonutChart">';
        }

        if (time_series != "")
            drawSteppedChart(time_series);
        else {
            document.getElementById("TimeSeriesChart").remove(); // remove canvas old chart
            document.getElementById("stepped-chart").innerHTML = '<canvas id="TimeSeriesChart">';
        }

        if (word_frequency != "")
            drawBarChart(word_frequency);
        else {
            document.getElementById("WordFrequencyChart").remove(); // remove canvas old chart
            document.getElementById("bar-chart").innerHTML = '<canvas id="WordFrequencyChart">';
        }
        if (top_10_retweeted != "")
            embedTopRetweeted(top_10_retweeted);
        else {
            document.getElementById("top-10-retweeted").innerHTML = "";
        }
        if (top_10_liked != "")
            embedTopLiked(top_10_liked);
        else {
            document.getElementById("top-10-liked").innerHTML = "";
        }

        return data;
    }
    data = getData();

})

function drawDonutChart(tweet_distribution) {
    document.getElementById("TweetSentimentDonutChart").remove();
    document.getElementById("donut-chart").innerHTML = '<canvas id="TweetSentimentDonutChart">';

    var positive = null;
    var negative = null;
    var neutral = null;
    for (var i = 0; i < tweet_distribution.length; i++) {
        if (tweet_distribution[i]["Sentiment"] == "Neutral")
            neutral = tweet_distribution[i]["Total Tweets"];
        else if (tweet_distribution[i]["Sentiment"] == "Positive")
            positive = tweet_distribution[i]["Total Tweets"];
        else negative = tweet_distribution[i]["Total Tweets"];
    }
    const data = {
        labels: [
            'Positive',
            'Negative',
            'Neutral'
        ],
        datasets: [{
            label: 'Tweets Sentiment Distribution',
            data: [positive, negative, neutral],
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
            ],
            hoverOffset: 4
        }]
    };
    const config = {
        type: 'doughnut',
        data: data,
        responsive: true,
        maintainAspectRatio: false
    };
    const chart = new Chart(document.getElementById("TweetSentimentDonutChart"), config);
    // new Chart(chart, config)

}

function drawSteppedChart(time_series) {
    document.getElementById("TimeSeriesChart").remove(); // remove canvas old chart
    document.getElementById("stepped-chart").innerHTML = '<canvas id="TimeSeriesChart">';
    var hour_of_day = ["0", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23"
    ];
    var count_by_time = new Array(24);
    for (var i = 0; i < time_series.length; i++) {
        var hour = time_series[i]["hour_created_at"];
        count_by_time[parseInt(hour)] = time_series[i]["counts"];
    }
    for (var i = 0; i < count_by_time.length; i++) {
        if (typeof(count_by_time[i]) == 'undefined')
            count_by_time[i] = 0;
    }
    console.log(count_by_time);
    console.log(hour_of_day);
    const data = {
        labels: hour_of_day,
        datasets: [{
            label: "Time Series of Tweets",
            data: count_by_time,
            fill: false,
            stepped: true,
        }]
    };
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            interaction: {
                intersect: false,
                axis: 'x'
            },
            plugins: {
                title: {
                    display: false,
                    text: (ctx) => 'Step ' + ctx.chart.data.datasets[0].stepped + ' Interpolation',
                }
            },
            scales: {
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Number of Tweets'
                    }
                },
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Hour of Day (GMT)'
                    }
                }
            },
            responsive: true,
            maintainAspectRatio: false

        }
    };
    const chart = new Chart(document.getElementById("TimeSeriesChart"), config);
}

function drawBarChart(word_frequency) {
    document.getElementById("WordFrequencyChart").remove(); // remove canvas old chart
    document.getElementById("bar-chart").innerHTML = '<canvas id="WordFrequencyChart">';
    var label_words = new Array(10);
    var words_count = new Array(10);
    for (var i = 0; i < 10; i++) {
        label_words[i] = word_frequency[i]["Words"];
        words_count[i] = word_frequency[i]["Count"];
    }
    const data = {
        labels: label_words,
        datasets: [{
            axis: 'y',
            label: 'Words Frequency',
            data: words_count,
            fill: false,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(153, 102, 255)',
                'rgb(201, 203, 207)'
            ],
            borderWidth: 1
        }]
    };
    const config = {
        type: 'bar',
        data,
        options: {
            indexAxis: 'y',
            responsive: true,
            interaction: {
                intersect: false,
                axis: 'x'
            },
            responsive: true,
            maintainAspectRatio: false
        }
    };
    const chart = new Chart(document.getElementById("WordFrequencyChart"), config);
}

function embedTopRetweeted(top_10_retweeted) {
    var top_10_retweeted_widget = document.getElementById("top-10-retweeted");
    top_10_retweeted_widget.innerHTML = "<p>Top 10 Retweeted Tweets</p>";
    for (var i = 0; i < 10; i++) {
        id = top_10_retweeted[i]["tweet_id"];
        tweet = `<blockquote class="twitter-tweet">
            <a href="https://twitter.com/x/status/${id}"></a>
            </blockquote><hr>`;
        top_10_retweeted_widget.innerHTML += tweet;
    }
    top_10_retweeted_widget.style.overflow = scroll;
    twttr.widgets.load(document.getElementById("top-10-retweeted")[0]);
}

function embedTopLiked(top_10_liked) {
    var top_10_liked_widget = document.getElementById("top-10-liked");
    top_10_liked_widget.innerHTML = "<p>Top 10 Liked Tweets</p>";
    for (var i = 0; i < 10; i++) {
        id = top_10_liked[i]["tweet_id"];
        tweet = `<blockquote class="twitter-tweet">
            <a href="https://twitter.com/x/status/${id}"></a>
            </blockquote>`;
        top_10_liked_widget.innerHTML += tweet;
    }
    //top_10_retweeted_widget.style.height = 500;
    top_10_liked_widget.style.overflow = scroll;
    twttr.widgets.load(document.getElementById("top-10-liked")[0]);

}