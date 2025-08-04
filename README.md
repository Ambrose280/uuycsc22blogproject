The database is in the 
/instance folder
/migrations is basically where datamodels are kept ypu dont need to tamper with that, its automatically configured by flask

/templates is where our html files will be kept

please only make pull requests and never commit to master until I approve

| Template              | Purpose                                 |
| --------------------- | --------------------------------------- |
| `register.html`       | User registration form                  |
| `login.html`          | Login form                              |
| `profile.html`        | Public profile view                     |
| `edit_profile.html`   | Profile update form                     |
| `create_post.html`    | New post creation form                  |
| `edit_post.html`      | Edit existing post                      |
| `post_detail.html`    | Full view of a single post              |
| `home.html`           | Homepage with post list & search        |
| `category_posts.html` | Posts by category                       |
| `search_results.html` | Posts by search                         |
| `_comments.html`      | Comment + reply section (partial)       |
| `bookmarks.html`      | View saved/bookmarked posts             |
| `base.html`           | Common layout (navigation, flash, etc.) |
| `404.html`            | Not found error page                    |
| `500.html`            | Internal error page                     |
