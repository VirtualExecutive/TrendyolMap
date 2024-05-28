using System.Windows.Forms;

namespace TrendyolMap
{
	partial class Form1
	{
		/// <summary>
		///Gerekli tasarımcı değişkeni.
		/// </summary>
		private System.ComponentModel.IContainer components = null;

		/// <summary>
		///Kullanılan tüm kaynakları temizleyin.
		/// </summary>
		///<param name="disposing">yönetilen kaynaklar dispose edilmeliyse doğru; aksi halde yanlış.</param>
		protected override void Dispose(bool disposing)
		{
			if (disposing && (components != null))
			{
				components.Dispose();
			}
			base.Dispose(disposing);
		}

		#region Windows Form Designer üretilen kod

		/// <summary>
		/// Tasarımcı desteği için gerekli metot - bu metodun 
		///içeriğini kod düzenleyici ile değiştirmeyin.
		/// </summary>
		private void InitializeComponent()
		{
			this.textBox1 = new System.Windows.Forms.TextBox();
			this.label1 = new System.Windows.Forms.Label();
			this.button1 = new System.Windows.Forms.Button();
			this.radioButtonMin = new System.Windows.Forms.RadioButton();
			this.radioButtonAvg = new System.Windows.Forms.RadioButton();
			this.radioButtonMax = new System.Windows.Forms.RadioButton();
			this.label2 = new System.Windows.Forms.Label();
			this.textBox2 = new System.Windows.Forms.TextBox();
			this.SuspendLayout();
			// 
			// textBox1
			// 
			this.textBox1.Location = new System.Drawing.Point(12, 37);
			this.textBox1.Name = "textBox1";
			this.textBox1.Size = new System.Drawing.Size(328, 20);
			this.textBox1.TabIndex = 1;
			// 
			// label1
			// 
			this.label1.AutoSize = true;
			this.label1.Location = new System.Drawing.Point(12, 18);
			this.label1.Name = "label1";
			this.label1.Size = new System.Drawing.Size(99, 13);
			this.label1.TabIndex = 2;
			this.label1.Text = "Trendyol Ürün Linki";
			// 
			// button1
			// 
			this.button1.Location = new System.Drawing.Point(12, 176);
			this.button1.Name = "button1";
			this.button1.Size = new System.Drawing.Size(139, 23);
			this.button1.TabIndex = 3;
			this.button1.Text = "Sonuçları Göster";
			this.button1.UseVisualStyleBackColor = true;
			this.button1.Click += new System.EventHandler(this.button1_Click);
			// 
			// radioButtonMin
			// 
			this.radioButtonMin.AutoSize = true;
			this.radioButtonMin.Location = new System.Drawing.Point(15, 107);
			this.radioButtonMin.Name = "radioButtonMin";
			this.radioButtonMin.Size = new System.Drawing.Size(123, 17);
			this.radioButtonMin.TabIndex = 4;
			this.radioButtonMin.TabStop = true;
			this.radioButtonMin.Text = "En Ucuz Fiyata Göre";
			this.radioButtonMin.UseVisualStyleBackColor = true;
			this.radioButtonMin.CheckedChanged += new System.EventHandler(this.RadioButton_CheckedChanged);
			// 
			// radioButtonAvg
			// 
			this.radioButtonAvg.AutoSize = true;
			this.radioButtonAvg.Location = new System.Drawing.Point(15, 130);
			this.radioButtonAvg.Name = "radioButtonAvg";
			this.radioButtonAvg.Size = new System.Drawing.Size(124, 17);
			this.radioButtonAvg.TabIndex = 5;
			this.radioButtonAvg.TabStop = true;
			this.radioButtonAvg.Text = "Ortalama Fiyata Göre";
			this.radioButtonAvg.UseVisualStyleBackColor = true;
			this.radioButtonAvg.CheckedChanged += new System.EventHandler(this.RadioButton_CheckedChanged);
			// 
			// radioButtonMax
			// 
			this.radioButtonMax.AutoSize = true;
			this.radioButtonMax.Location = new System.Drawing.Point(15, 153);
			this.radioButtonMax.Name = "radioButtonMax";
			this.radioButtonMax.Size = new System.Drawing.Size(127, 17);
			this.radioButtonMax.TabIndex = 6;
			this.radioButtonMax.TabStop = true;
			this.radioButtonMax.Text = "En Pahalı Fiyata Göre";
			this.radioButtonMax.UseVisualStyleBackColor = true;
			this.radioButtonMax.CheckedChanged += new System.EventHandler(this.RadioButton_CheckedChanged);
			// 
			// label2
			// 
			this.label2.AutoSize = true;
			this.label2.Location = new System.Drawing.Point(12, 80);
			this.label2.Name = "label2";
			this.label2.Size = new System.Drawing.Size(287, 13);
			this.label2.TabIndex = 7;
			this.label2.Text = "Birden fazla satıcısı olan aynı ilçede neye göre hesaplansın?";
			// 
			// textBox2
			// 
			this.textBox2.Location = new System.Drawing.Point(406, 18);
			this.textBox2.Multiline = true;
			this.textBox2.Name = "textBox2";
			this.textBox2.ReadOnly = true;
			this.textBox2.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
			this.textBox2.Size = new System.Drawing.Size(360, 181);
			this.textBox2.TabIndex = 8;
			// 
			// Form1
			// 
			this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.ClientSize = new System.Drawing.Size(376, 216);
			this.Controls.Add(this.textBox2);
			this.Controls.Add(this.label2);
			this.Controls.Add(this.radioButtonMax);
			this.Controls.Add(this.radioButtonAvg);
			this.Controls.Add(this.radioButtonMin);
			this.Controls.Add(this.button1);
			this.Controls.Add(this.label1);
			this.Controls.Add(this.textBox1);
			this.Name = "Form1";
			this.Text = "Trendyol Map";
			this.Load += new System.EventHandler(this.Form1_Load);
			this.ResumeLayout(false);
			this.PerformLayout();

		}

		#endregion
		private System.Windows.Forms.TextBox textBox1;
		private System.Windows.Forms.Label label1;
		private System.Windows.Forms.Button button1;
		private System.Windows.Forms.RadioButton radioButtonMin;
		private System.Windows.Forms.RadioButton radioButtonAvg;
		private System.Windows.Forms.RadioButton radioButtonMax;
		private System.Windows.Forms.Label label2;
		private System.Windows.Forms.TextBox textBox2;
	}
}

