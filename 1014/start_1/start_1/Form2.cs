using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using NAudio.CoreAudioApi;
using NAudio.Wave;


namespace start_1
{
    public partial class Form1 : Form
    {
        Dictionary<string, string> micNames;
        public Form1()
        {
            //マイク検出
            /*
            InitializeComponent();

            this.micNames = new Dictionary<string, string>();

            var enumerator = new MMDeviceEnumerator();

            //for (int i = 1; i<11; i++)
            //{ 
            //    this.micNames.Add(string.Format("マイク{0}", i), i.ToString());
            //}

            foreach (var endpoint in
                     enumerator.EnumerateAudioEndPoints(DataFlow.Capture, DeviceState.Active))
            {
                //Console.WriteLine("{0} ({1})", endpoint.FriendlyName, endpoint.ID);
                this.micNames.Add(endpoint.FriendlyName, endpoint.ID);
            }


            foreach (KeyValuePair<string, string> data in this.micNames)
            {
                micBox.Items.Add(data.Key);
            }
            */
            //ここまで

            //マイク検出2
            InitializeComponent();
            MMDeviceEnumerator enumerator = new MMDeviceEnumerator();
            var devices = enumerator.EnumerateAudioEndPoints(DataFlow.All, DeviceState.Active);
            comboBox1.Items.AddRange(devices.ToArray());

            //スピーカー検出
            WaveOut waveOut = new WaveOut();
            List<string> spkList = new List<string>();
            for (int i = 0; i < WaveOut.DeviceCount; i++)
            {
                var capabilities = WaveOut.GetCapabilities(i);
                spkList.Add(capabilities.ProductName);
            }
            foreach (String data in spkList)
            {
                spkBox.Items.Add(data);
            }

        }

        
        private void micSelected(object sender, EventArgs e)
        {
             //マイク選択
        }

        private void ExitMenueClicked(object sender, EventArgs e)
        {
            //終了メニュー
            this.Close();
        }

        private void spkSelected(object sender, EventArgs e)
        {
            //スピーカー選択
            Console.WriteLine("SelectedIndex:{0}", spkBox.SelectedIndex);

        }

        WaveOut wave = null;
        private void button1_Click(object sender, EventArgs e)
        {
            
            // "既定の" デバイスで音を出すコード
            //System.Media.SoundPlayer simpleSound = new System.Media.SoundPlayer(@"c:\Windows\Media\chimes.wav");
            //simpleSound.Play();
            //ここまで


            //スピーカーのテストボタンを押したとき、PlaySoubd関数へ
            //ここから
            int DeviceNumber = spkBox.SelectedIndex;//選択したデバイス情報;
            PlaySound(DeviceNumber);//関数呼び出し
            
            //ここまで

        }

        //マイクのメーター処理
        private void timer1_Tick(object sender, EventArgs e)
        {
            if (comboBox1.SelectedItem != null)
            {
                var device = (MMDevice)comboBox1.SelectedItem;
                progressBar1.Value = (int)(Math.Round(device.AudioMeterInformation.MasterPeakValue * 100));
            }

        }

        //ここから
        // "指定の" デバイスで音を出すPlaySoubd関数
        private void PlaySound(int deviceNumber)
        {
            //var waveReader = new NAudio.Wave.WaveFileReader(filePath);
            //var waveOut = new NAudio.Wave.WaveOut();
            //waveOut.DeviceNumber =0;

            //waveOut.Init(@"c:\Windows\Media\chimes.wav");
            //System.Media.SoundPlayer simpleSound = new System.Media.SoundPlayer(@"c:\Windows\Media\chimes.wav");
            //waveOut.Play();
            //simpleSound.Play();

            var waveReader = new NAudio.Wave.WaveFileReader(@"c:\Windows\Media\chimes.wav");
            var waveOut = new NAudio.Wave.WaveOut();
            waveOut.DeviceNumber = deviceNumber;
            waveOut.Init(waveReader);
            waveOut.Play();
        }

        private void 録音画面へToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //メニューバーの録音画面へをクリック時

            //現在画面を閉じる
            this.Visible = false;

            //録音画面へ遷移
            Form3 form3 = new Form3(this);
            form3.Show();
        }
        //ここまで
    }
}
