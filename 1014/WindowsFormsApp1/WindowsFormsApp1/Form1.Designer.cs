namespace WindowsFormsApp1
{
    partial class Form1
    {
        /// <summary>
        /// 必要なデザイナー変数です。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 使用中のリソースをすべてクリーンアップします。
        /// </summary>
        /// <param name="disposing">マネージド リソースを破棄する場合は true を指定し、その他の場合は false を指定します。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows フォーム デザイナーで生成されたコード

        /// <summary>
        /// デザイナー サポートに必要なメソッドです。このメソッドの内容を
        /// コード エディターで変更しないでください。
        /// </summary>
        private void InitializeComponent()
        {
            this.押してボタン = new System.Windows.Forms.Button();
            this.henji = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // 押してボタン
            // 
            this.押してボタン.Location = new System.Drawing.Point(267, 248);
            this.押してボタン.Name = "押してボタン";
            this.押してボタン.Size = new System.Drawing.Size(152, 56);
            this.押してボタン.TabIndex = 0;
            this.押してボタン.Text = "押してみるかい？";
            this.押してボタン.UseVisualStyleBackColor = true;
            this.押してボタン.Click += new System.EventHandler(this.押してボタンClicked);
            // 
            // henji
            // 
            this.henji.AutoSize = true;
            this.henji.Location = new System.Drawing.Point(292, 128);
            this.henji.Name = "henji";
            this.henji.Size = new System.Drawing.Size(69, 12);
            this.henji.TabIndex = 1;
            this.henji.Text = " 絶対だめよ。";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.henji);
            this.Controls.Add(this.押してボタン);
            this.Name = "Form1";
            this.Text = "Form1";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button 押してボタン;
        private System.Windows.Forms.Label henji;
    }
}

