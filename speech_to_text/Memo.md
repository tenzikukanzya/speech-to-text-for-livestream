# 本体

### ChatGPT

#### root

##### \_\_main\_\_.py
`__main__.py` ファイルは、アプリケーションのエントリーポイントとして機能します。ここには、Eelを使用してGUIを表示し、音声からテキストへの変換を制御するための主要な関数やロジックが記述されています。

以下に、主要な機能とその役割についての詳細を提供します。

1. `get_valid_devices()`: 使用可能な音声デバイスのリストを取得します。

2. `get_dropdown_options()`: ドロップダウンリストのオプションを取得します。

3. `get_user_settings()`: ユーザーの設定を取得します。

4. `start_transcription(user_settings)`: ユーザーの設定に基づいて音声からテキストへの変換を開始します。

5. `stop_transcription()`: 音声からテキストへの変換を停止します。

6. `audio_transcription(user_settings, base64data)`: 音声データ（Base64形式）をテキストに変換します。

7. `get_filtered_app_settings(settings)`, `get_filtered_model_settings(settings)`, `get_filtered_transcribe_settings(settings)`: 設定から特定のキーをフィルタリングします。

8. `extracting_each_setting(user_settings)`: ユーザーの設定からアプリケーション設定、モデル設定、および変換設定を抽出します。

9. `on_close(page, sockets)`: ページが閉じられたときの処理を定義します。

このファイルの最後には、`eel.start()` 関数が呼び出されており、これによりGUIが表示されます。また、`close_callback` パラメータに `on_close` 関数が渡されているため、ウィンドウが閉じられたときには音声からテキストへの変換が停止します。

##### audio_transcriber.py

`audio_transcriber.py`ファイルについて確認します。

`audio_transcriber.py` ファイルは、音声からテキストへの変換を管理する主要なクラス `AudioTranscriber` を定義しています。以下に、その主要なメソッドと役割について説明します。

1. `__init__(self, event_loop, whisper_model, transcribe_settings, app_options, websocket_server, openai_api)`: コンストラクタでは、いくつかの重要なオブジェクトと設定がインスタンス変数として保存されます。

2. `transcribe_audio(self)`: この非同期メソッドは、音声データのキューから音声データを取得し、それをテキストに変換します。

3. `process_audio(self, audio_data, frames, time, status)`: このメソッドは、音声データを受け取り、音声活動検出（VAD）を使用して音声と無音を区別します。

4. `batch_transcribe_audio(self, audio_data)`: このメソッドは、大量の音声データを一度にテキストに変換します。

5. `text_proofreading(self, segment_list)`: このメソッドは、変換されたテキストの校正を行います。

6. `start_transcription(self)`: この非同期メソッドは、音声からテキストへの変換を開始します。音声ストリームが作成され、変換タスクが開始されます。

7. `stop_transcription(self)`: この非同期メソッドは、音声からテキストへの変換を停止します。音声ストリームが停止され、変換タスクがキャンセルされます。

このクラスは、音声データの取得、音声からテキストへの変換、変換結果の表示や送信など、アプリケーションの主要な機能を管理します。

#### utils

##### audio_utils.py
`audio_utils.py`ファイルは、音声データの取得と処理に関連するいくつかのユーティリティ関数を提供しています。以下に、各関数の詳細な解説をします。

1. `get_valid_input_devices()`: この関数は、入力として使用可能な音声デバイスのリストを取得します。関数内部で、`sounddevice`ライブラリの`query_devices()`と`query_hostapis()`メソッドを使用して、音声デバイスとホストAPIの情報を取得します。

2. `create_audio_stream(selected_device, callback)`: 選択されたデバイスとコールバック関数を引数に取り、音声ストリームを作成します。作成された音声ストリームは、選択されたデバイスから音声データを非同期に取得します。この関数は、`sounddevice`ライブラリの`InputStream`クラスを使用して音声ストリームを作成します。

3. `base64_to_audio(audio_data)`: この関数は、Base64形式の音声データを受け取り、それをオーディオファイルに変換します。変換は、`soundfile`ライブラリの`read`メソッドと`librosa`ライブラリの`resample`メソッドを使用して行います。

これらの関数は、音声データの取得、音声ストリームの作成、音声データの変換など、音声をテキストに変換するアプリケーションにおける重要な操作を助けます。

##### file_utils.py

`file_utils.py`ファイルは、ファイル操作に関連するユーティリティ関数を提供しています。以下に、各関数の詳細な解説をします。

1. `read_json(dir_name: str, json_name: str)`: この関数は、指定されたディレクトリとJSONファイル名を引数に取り、そのJSONファイルを読み込みます。読み込んだデータはPythonの辞書として返されます。

2. `write_json(dir_name: str, json_name: str, data: dict)`: この関数は、指定されたディレクトリ、JSONファイル名、およびデータ（辞書）を引数に取り、データをJSONファイルとして書き出します。

3. `write_audio(dir_name: str, file_name: str, data)`: この関数は、指定されたディレクトリ、ファイル名、およびデータ（numpy配列など）を引数に取り、データを音声ファイル（WAV形式）として書き出します。すでに同名のファイルが存在する場合は、そのファイルを削除して新しいファイルを強制的に書き出します。

これらの関数は、JSONデータの読み書き、音声データの書き出しといった、ファイル操作に関連する一般的な操作を容易にします。