const contentData = {
    home: {
        title: "Wikipedia Product Analysis Dashboard",
        subtitle: "Comprehensive analysis of pageviews, editor trends, and social sentiment (2015–2025)",
        html: `
            <div class="wiki-box">
                <p><strong>Welcome to the Wikipedia Product Analysis Dashboard.</strong> This project explores the health and reach of Wikipedia through multi-dimensional data analysis.</p>
                <p>Navigate through the menu on the left to explore different facets of the analysis, including:</p>
                <ul>
                    <li><strong>Pageview Analysis:</strong> Interactive trends and seasonality analysis of Wikipedia traffic across time.</li>
                    <li><strong>Reddit Sentiment Analysis:</strong> Insights into public perception of Wikipedia and ChatGPT based on Reddit discussions.</li>
                    <li><strong>Twitter Sentiment Analysis:</strong> Analysis of public sentiment on Twitter regarding Wikipedia.</li>
                </ul>
            </div>
        `
    },
    pageviews: {
        title: "Wikipedia Pageview Analysis (2015–2025)",
        subtitle: "Interactive Tableau Dashboard for regional and platform-level insights",
        html: `
            <div class="dashboard-container">
                <div class='tableauPlaceholder' id='viz1773934367186' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;wi&#47;wikipediapageviewanalysis&#47;pageviewanalysis&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='wikipediapageviewanalysis&#47;pageviewanalysis' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;wi&#47;wikipediapageviewanalysis&#47;pageviewanalysis&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1773934367186');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='1000px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='850px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='1000px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='850px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.minHeight='1400px';vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
            </div>
            <div class="wiki-box insights-section">
                <h2>Data Insights & Analysis</h2>
                <div class="insight-item">
                    <h3>1. Weekend vs Weekday Usage</h3>
                        <p>
                            Wikipedia was primarily a <strong>weekday-driven utility before 2020</strong>, with higher activity during school and workdays (ratio &lt; 1.0). Over time, the ratio steadily increases and crosses 1.0 during the pandemic, remaining above it, indicating rising weekend activity. This suggests an evolving usage pattern, where <strong>remote and flexible work may have shifted traditional school- and work-driven traffic spikes</strong>.
                        </p>
                    <h3>2. Wikipedia Seasonality</h3>
                        <p>
                            Wikipedia traffic shows a <strong>stable seasonal pattern with a strong baseline (7–8B pageviews)</strong>, where <strong>June consistently records the lowest pageviews and January shows comparatively higher activity</strong>, reflecting predictable user behavior cycles. Wikipedia’s traffic demonstrates <strong>dual drivers</strong>: a stable seasonal structure tied to academic calendars and information-seeking behavior, combined with <strong>unpredictable spikes from major world events</strong>, highlighting its resilience in maintaining a consistent multi-billion pageview baseline despite external shocks. However, recent years indicate a <strong>slight downward shift from the 2020–2022 peak</strong>, suggesting normalization after pandemic-driven demand, with a <strong>minor emerging influence of AI-mediated information access</strong> shaping future growth.
                        </p>
                    <h3>3. Campaign Impact on Traffic</h3>
                        <p>
                            Across campaign types, pageview lift remains within a relatively narrow range (around -6% to +7%), indicating that overall impact on Wikipedia traffic is moderate. Median effects cluster near zero, suggesting campaigns do not drastically alter total usage. However, <strong>community-driven initiatives like Wikipedia Asian Month show relatively stronger positive engagement signals</strong> compared to fundraising or photography campaigns. Campaigns have limited direct impact on overall pageview volume, as most of them, especially fundraising ones, target existing users and prioritize conversion over traffic growth, reflecting a different product objective rather than a lack of effectiveness.
                        </p>
                        <h3>4. Topic-Based Seasonal Behavior</h3>
                        <p>
                            Different content domains on Wikipedia exhibit distinct seasonal patterns. Education-related content follows strong academic cycles, political content shows moderate variation linked to real-world events, while entertainment remains relatively stable with weaker seasonality. This highlights a dual role of Wikipedia: it functions as a <strong>structured academic reference driven by school and work cycles</strong>, while also serving as a <strong>steady source of general and event-driven information</strong>. These patterns indicate that user intent varies by domain, and growth in one category is unlikely to cannibalize others, suggesting opportunities for cross-domain engagement.
                        </p>
            </div>
            <div class="footer">Interactive dashboard powered by Tableau Public</div>
        `,
        callback: () => {
            var divElement = document.getElementById('viz1773934367186');
            var vizElement = divElement.getElementsByTagName('object')[0];
            vizElement.style.width = '100%';
            vizElement.style.height = (divElement.offsetWidth * 0.75) + 'px';
            var scriptElement = document.createElement('script');
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
            vizElement.parentNode.insertBefore(scriptElement, vizElement);
        }
    },
    "Reddit sentiment analysis": {
        title: "Reddit Sentiment Analysis",
        subtitle: "Interactive Tableau Dashboard for regional and platform-level insights",
        html: `
            <div class="dashboard-container">
                <div class='tableauPlaceholder' id='viz1773927011080' style='position: relative'><noscript><a href='#'><img alt='Reddit Dash ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Re&#47;Reddit_Dashboard&#47;RedditDash&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Reddit_Dashboard&#47;RedditDash' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Re&#47;Reddit_Dashboard&#47;RedditDash&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1773927011080');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1827px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
            </div>
            <div class="wiki-box insights-section">
                <h2>Data Insights & Analysis</h2>
                
                <div class="insight-item">
                    <h3>1. Post Volume Surge (Pre vs. Post ChatGPT)</h3>
                    <p>The launch of ChatGPT triggered a massive surge in discussions across AI and tech-related subreddits. Subreddits like <strong>r/singularity</strong>, <strong>r/technology</strong>, and <strong>r/wikipedia</strong> saw exponential growth in activity post-launch discussing the impact of AI on wikipedia, indicating a transformative shift in public interest toward generative AI.</p>
                </div>

                <div class="insight-item">
                    <h3>2. Sentiment Volatility & Trends</h3>
                    <p>While discussion volume increased, the average sentiment (Roberta Continuous) exhibited significant volatility. A noticeable dip in sentiment scores occurred immediately following the ChatGPT launch, suggesting that the massive influx of new users and broader public debate brought about more critical, cautious, or polarized perspectives on AI and Wikipedia compared to the earlier, more specialized discourse.</p>
                </div>

                <div class="insight-item">
                    <h3>3. Subreddit-Specific Sentiment</h3>
                    <ul>
                        <li><strong>Specialized Communities:</strong> Subreddits like <em>r/MachineLearning</em> and <em>r/artificial</em> maintain a generally positive or neutral outlook, focused on technical progress.</li>
                        <li><strong>General Tech Communities:</strong> <em>r/technology</em> and <em>r/wikipedia</em> exhibit more negative average sentiment, likely reflecting broader societal concerns regarding ethics, misinformation, LLM hallucinations and AI "hype."</li>
                    </ul>
                </div>

                <div class="insight-item">
                    <h3>4. Model Comparison: ROBERTA vs. VADER</h3>
                    <p>The sentiment classification analysis reveals that while both models agree on <strong>Neutral</strong> sentiment (high correlation), the <strong>ROBERTA</strong> transformer model provides more nuanced detection of negative sentiment compared to the lexicon-based <strong>VADER</strong>. Discrepancies often occur in complex social media text where sarcasm or technical context is present, highlighting ROBERTA's superior performance for this dataset.</p>
                    <p>This was done just to test how VADER and ROBERTA models worked and how they differed from each other.</p>
                </div>
            </div>
            <div class="footer">Interactive dashboard powered by Tableau Public</div>
        `,
        callback: () => {
            var divElement = document.getElementById('viz1773927011080');
            var vizElement = divElement.getElementsByTagName('object')[0];
            vizElement.style.width = '100%';
            vizElement.style.height = (divElement.offsetWidth * 0.75) + 'px';
            var scriptElement = document.createElement('script');
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
            vizElement.parentNode.insertBefore(scriptElement, vizElement);
        }
    },

};

function renderContent(key) {
    const data = contentData[key];
    const header = document.querySelector('header');
    const container = document.getElementById('main-container');

    // Update Header
    header.innerHTML = `
        <h1>${data.title}</h1>
        <div class="subtitle">${data.subtitle}</div>
    `;

    // Update Content
    container.innerHTML = data.html;

    // Run Callback if exists
    if (data.callback) {
        data.callback();
    }

    // Update Sidebar Active State
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-tab') === key) {
            item.classList.add('active');
        }
    });

    // Scroll to top
    window.scrollTo(0, 0);
}

document.addEventListener('DOMContentLoaded', () => {
    // Initial Render
    renderContent('home');

    // Event Listeners for Sidebar
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', (e) => {
            const key = e.target.getAttribute('data-tab');
            if (key) {
                renderContent(key);
            }
        });
    });
});
