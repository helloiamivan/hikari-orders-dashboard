import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event
import pandas as pd
import dropbox
from io import StringIO

VALID_USERNAME_PASSWORD_PAIRS = [
    ['hikari', 'mobility']
]

app = dash.Dash('Hikari')
server = app.server
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

dbx = dropbox.Dropbox('LwFnruIQkGAAAAAAAAAALwpMo4HhE7VCXwhU3BzGHq58eBTQLORBx5mgf0_oPR9t')

def update_table(max_rows=1000):
	coinsFile = ['BTC','ETH','ETHBTC']

	for coin in coinsFile:
		path = '/hikari-clientside-py-telegram-bot/Output/OrderBooks/' + coin +'.csv'
		md, res = dbx.files_download(path)
		data = StringIO(str(res.content,'utf-8'))

		temp_df= pd.read_csv(data,header=None)
		temp_df.columns = ['OrderID','Side','User','Coin','Quantity','Price','Expiry','Time','Epoch_Time','Status']

		try:
			df = pd.concat([df,temp_df],ignore_index=True)
		except:
			df = temp_df

	df.sort_values(by=['Epoch_Time'],ascending=False,inplace=True)

	return html.Table(
	# Header
	[html.Tr([html.Th(col) for col in df.columns])] +

	# Body
	[html.Tr([
		html.Td(df.iloc[i][col]) for col in df.columns
	]) for i in range(min(len(df), max_rows))]
	)

def serve_layout():
	return html.Div(children=[html.H4(children='List of Hikari Orders'),update_table()])

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)