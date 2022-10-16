from flask import Flask, request
import pickle
import numpy as np
import os

pt_table = pickle.load(open('pt_table.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_count = pickle.load(open('similarity_count.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return "Hellow World!!!"

@app.route('/predict',methods = ['POST'])
def predict():

    bookname = request.form.get('bookname')

    index = np.where(pt_table.index == bookname)[0][0]
    similar_items = sorted(list(enumerate(similarity_count[index])), key=lambda x: x[1], reverse=True)[1:11]

    data = []

    for i in similar_items:
        item = []
        temp_df = books[books['bookname'] == pt_table.index[i[0]]]
        temp_df = temp_df.fillna(0)
        item.extend(list(temp_df.drop_duplicates('bookname')['bookname'].values))

        data.append(item)


    return str(data)

port = int(os.environ.get("PORT", 5001))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)