from bottle import route,run,view,static_file,redirect,request
from db import TodoItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
s = Session()

@route('/static/<filename:path>')
def send_static(filename):
	return static_file(filename, root='static')

@route('/')
@view('index')
def index():
	total_tasks = s.query(TodoItem).count()
	incomplete_tasks = s.query(TodoItem).filter(TodoItem.is_completed == False).count()
	tasks = s.query(TodoItem).order_by(TodoItem.uid)
	return {'tasks':tasks,
			'total_tasks': total_tasks,
			'incomplete_tasks': incomplete_tasks,
			}

@route('/api/delete/<uid:int>')
def api_delete(uid):
	s.query(TodoItem).filter(TodoItem.uid == uid).delete()
	s.commit()
	return redirect('/')

@route('/api/complete/<uid:int>')
def api_complete(uid):
	t = s.query(TodoItem).filter(TodoItem.uid == uid).first()
	t.is_completed = True
	s.commit()
	return 'Ok'
	# return redirect('/')

@route('/add-task', method='POST')
def add_task():
	desc = request.POST.description.strip()	# поле POST-запроса description совпадает с именем
											# формы из страницы HTML (<input class='form-control' name='description'>)
	incomplete_tasks = s.query(TodoItem).filter(TodoItem.is_completed == False).count()
	if len(desc) > 0 and incomplete_tasks < 10:
		t = TodoItem(desc)
		s.add(t)
		s.commit()
	return redirect('/')

run(
	host='localhost',
	port=8080
	)

