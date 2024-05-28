using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TrendyolMap
{
	public partial class Form1 : Form
	{
		string yontem = "min";
		public Form1()
		{
			InitializeComponent();
		}

		private void Form1_Load(object sender, EventArgs e)
		{

		}

		private void button1_Click(object sender, EventArgs e)
		{
			button1.Enabled = false;
			RunPythonScript("main.py", new string[] { textBox1.Text}, "./Python/TrendyolMiner");
			RunPythonScript("main.py", new string[] { textBox1.Text, yontem }, "./Python/TrendyolMap");
			button1.Enabled = true;
		}

		private void RadioButton_CheckedChanged(object sender, EventArgs e)
		{
			RadioButton radioButton = sender as RadioButton;
			if (radioButton.Checked)
			{
				switch (radioButton.Name) 
				{
					case "radioButtonMin": { yontem = "min"; break; }
					case "radioButtonAvg": { yontem = "avg"; break; }
					case "radioButtonMax": { yontem = "max"; break; }
				}
			}
		}
		private void RunPythonScript(string scriptPath, string[] inputs, string workingDirectory)
		{
			try
			{
				// Python dosyasını çalıştırmak için ProcessStartInfo oluştur
				ProcessStartInfo start = new ProcessStartInfo();
				start.FileName = "py"; // Python'un kurulu olduğu yola göre değiştirin
				start.Arguments = $"{scriptPath} {string.Join(" ", inputs)}";
				start.WorkingDirectory = workingDirectory;
				start.UseShellExecute = false;
				start.RedirectStandardOutput = true;
				start.RedirectStandardError = true;
				start.CreateNoWindow = true;

				// Process'i başlat ve çıktıları oku
				using (Process process = Process.Start(start))
				{
					using (StreamReader reader = process.StandardOutput)
					{
						string result = reader.ReadToEnd();
						// Çıktıyı TextBox'a ekleyin
						Invoke(new Action(() => textBox2.AppendText(result + Environment.NewLine)));
					}

					using (StreamReader errorReader = process.StandardError)
					{
						string error = errorReader.ReadToEnd();
						if (!string.IsNullOrEmpty(error))
						{
							// Hata varsa TextBox'a ekleyin
							Invoke(new Action(() => textBox2.AppendText("Error: " + error + Environment.NewLine)));
						}
					}
				}
			}
			catch (Exception ex)
			{
				// İstisna durumunu TextBox'a ekleyin
				Invoke(new Action(() => textBox2.AppendText("Exception: " + ex.Message + Environment.NewLine)));
			}
		}
	}
}
