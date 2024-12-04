from app import app
import logging
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]'
)
file_handler.setFormatter(formatter)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
if __name__=="__main__":
    app.run(debug=True)